import asyncio
import logging
import json
from aiohttp import ClientSession, ClientWebSocketResponse, ClientError, WSMsgType
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_call_later
from .const import DOMAIN, EVENT_TYPE_IN, EVENT_TYPE_OUT

_LOGGER = logging.getLogger(__name__)

# Configuration for faster detection and reconnection
RECONNECT_DELAY = 5  # seconds
PING_INTERVAL = 5  # seconds


class MyDeviceWebSocketClient:
    def __init__(self, hass: HomeAssistant, host: str, port: int, serial: str, json_data: dict = None):
        self.hass = hass
        self.host = host
        self.port = port
        self.serial = serial
        self.ws: ClientWebSocketResponse | None = None
        self.listen_task: asyncio.Task | None = None
        self.ping_task: asyncio.Task | None = None
        self._session = ClientSession()
        self._reconnect_callback = None
        self._stop = False
        self.json_data = json_data or {}

    async def connect(self):
        url = f"ws://{self.host}:8080"
        _LOGGER.info("Attempting to connect to WebSocket at %s", url)

        while not self._stop:
            try:
                self.ws = await self._session.ws_connect(url)
                _LOGGER.info("Connected to WebSocket at %s", url)

                # Re-send initial configuration upon reconnection
                self.send_initial_config_to_event_bus()

                self.start_listening()
                self.start_ping()
                return

            except (ClientError, Exception) as e:
                _LOGGER.error("Failed to connect to %s: %s", url, e)
                _LOGGER.info("Retrying connection in %s seconds...", RECONNECT_DELAY)
                await asyncio.sleep(RECONNECT_DELAY)

    def start_listening(self):
        if not self.listen_task or self.listen_task.done():
            self.listen_task = self.hass.loop.create_task(self._listen())

    async def _listen(self):
        if not self.ws:
            return

        try:
            async for msg in self.ws:
                if msg.type == WSMsgType.TEXT:
                    data = msg.data
                    try:
                        event_data = json.loads(data)
                        event_data["serial"] = self.serial

                        # Check for "Not configured" status
                        if (
                            event_data.get("event", {}).get("type") == "status"
                            and event_data["event"].get("state") == "Not configured"
                        ):
                            _LOGGER.info("Device reported 'Not configured', resending initial config.")
                            self.send_initial_config_to_event_bus()

                        # Forward event to Home Assistant event bus
                        self.hass.bus.async_fire(EVENT_TYPE_IN, event_data)
                        _LOGGER.debug("Received event data %s: %s", self.serial, event_data)

                    except json.JSONDecodeError:
                        _LOGGER.warning("Received invalid JSON: %s", data)
                elif msg.type in (WSMsgType.CLOSED, WSMsgType.ERROR):
                    _LOGGER.warning("WebSocket closed, scheduling reconnect")
                    self.schedule_reconnect()
                    return

        except asyncio.CancelledError:
            _LOGGER.debug("Listening task was cancelled.")
        except Exception as e:
            _LOGGER.error("Error in WebSocket listen task: %s", e)
            self.schedule_reconnect()

    def start_ping(self):
        """Start sending WebSocket pings periodically."""
        if not self.ping_task or self.ping_task.done():
            self.ping_task = self.hass.loop.create_task(self._ping())

    async def _ping(self):
        """Send periodic pings to keep the WebSocket alive."""
        while not self._stop and self.ws:
            try:
                await self.ws.ping()
                _LOGGER.debug("Sent WebSocket ping")
            except Exception as e:
                _LOGGER.error("WebSocket ping failed: %s", e)
                self.schedule_reconnect()
                return
            await asyncio.sleep(PING_INTERVAL)

    def send_initial_config_to_event_bus(self):
        """Send the initial configuration to Home Assistant event bus."""
        if isinstance(self.json_data, dict):
            event_data = {
                **self.json_data,
                "serial": self.serial,
            }
            self.hass.bus.async_fire(EVENT_TYPE_OUT, event_data)
            _LOGGER.info("Sent initial configuration to event bus: %s", event_data)

    def schedule_reconnect(self):
        if self._stop:
            return

        if self._reconnect_callback:
            _LOGGER.debug("Cancelling previous reconnect attempt")
            self._reconnect_callback = None

        _LOGGER.info("Scheduling WebSocket reconnect in %s seconds", RECONNECT_DELAY)
        self._reconnect_callback = async_call_later(
            self.hass, RECONNECT_DELAY, self._async_reconnect
        )

    async def _async_reconnect(self, _now):
        _LOGGER.info("Reconnecting to WebSocket...")
        self._reconnect_callback = None
        await self.connect()

    async def send_message(self, message: dict | str):
        """Send a message over the WebSocket."""
        if not self.ws or self.ws.closed:
            _LOGGER.error("Cannot send message; WebSocket is not connected.")
            return

        try:
            if isinstance(message, str):
                message = json.loads(message)

            if not isinstance(message, dict):
                _LOGGER.error("Invalid message format. Expected a dictionary.")
                return

            await self.ws.send_str(json.dumps(message))
            _LOGGER.debug("Sent message to device %s: %s", self.serial, message)

        except json.JSONDecodeError as e:
            _LOGGER.error("JSON encoding error: %s. Message: %s", e, message)
        except Exception as e:
            _LOGGER.error("Failed to send message to device: %s", e)

    async def disconnect(self):
        """Disconnect from the WebSocket."""
        self._stop = True

        if self._reconnect_callback:
            _LOGGER.debug("Cancelling scheduled reconnect")
            self._reconnect_callback = None

        if self.listen_task and not self.listen_task.done():
            self.listen_task.cancel()

        if self.ping_task and not self.ping_task.done():
            self.ping_task.cancel()

        if self.ws and not self.ws.closed:
            _LOGGER.info("Closing WebSocket connection")
            await self.ws.close()

        if not self._session.closed:
            _LOGGER.info("Closing aiohttp session")
            await self._session.close()

        _LOGGER.info("WebSocket client disconnected.")