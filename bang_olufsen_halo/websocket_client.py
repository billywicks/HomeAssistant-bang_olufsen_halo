import asyncio
import logging
import json
from aiohttp import ClientSession, ClientWebSocketResponse
from homeassistant.core import HomeAssistant, CALLBACK_TYPE
from homeassistant.helpers.event import async_call_later
from .const import DOMAIN, EVENT_TYPE_IN

_LOGGER = logging.getLogger(__name__)

RECONNECT_DELAY = 10  # seconds

class MyDeviceWebSocketClient:
    def __init__(self, hass: HomeAssistant, host: str, port: int, serial: str):
        self.hass = hass
        self.host = host
        self.port = port
        self.serial = serial
        self.ws: ClientWebSocketResponse | None = None
        self.listen_task: asyncio.Task | None = None
        self._session = ClientSession()
        self._reconnect_callback: CALLBACK_TYPE | None = None
        self._stop = False

    async def connect(self):
        url = f"ws://{self.host}:8080"
        _LOGGER.debug("Attempting to connect to %s", url)
        try:
            self.ws = await self._session.ws_connect(url)
            _LOGGER.info("Connected to My Device WebSocket at %s", url)
        except Exception as e:
            _LOGGER.error("Failed to connect to %s: %s", url, e)
            self.schedule_reconnect()

    def start_listening(self):
        if self.listen_task is None or self.listen_task.done():
            self.listen_task = self.hass.loop.create_task(self._listen())

    async def _listen(self):
        if not self.ws:
            return

        async for msg in self.ws:
            if msg.type == 1:  # TEXT message
                data = msg.data
                try:
                    event_data = json.loads(data)
                    # Append the host to the event data
                    event_data["serial"] = self.serial
                    # Forward the event to Home Assistant's event bus
                    self.hass.bus.async_fire(EVENT_TYPE_IN, event_data)
                    _LOGGER.debug("Sending event data %s: %s", self.serial, event_data)
                except json.JSONDecodeError:
                    _LOGGER.warning("Received invalid JSON: %s", data)

        # If we get here, the websocket connection was closed
        _LOGGER.warning("WebSocket connection closed, scheduling reconnect")
        self.schedule_reconnect()

    def schedule_reconnect(self):
        if self._stop:
            return
        if self._reconnect_callback is not None:
            self._reconnect_callback()
        self._reconnect_callback = async_call_later(self.hass, RECONNECT_DELAY, self._async_reconnect)

    async def _async_reconnect(self, _now):
        self._reconnect_callback = None
        await self.connect()
        if self.ws:
            self.start_listening()

    async def send_message(self, message: dict):
        if self.ws is None or self.ws.closed:
            _LOGGER.error("Cannot send message, websocket not connected.")
            return
        await self.ws.send_str(json.dumps(message))
        
    async def disconnect(self):
        self._stop = True
        if self.listen_task and not self.listen_task.done():
            self.listen_task.cancel()
        if self.ws and not self.ws.closed:
            await self.ws.close()
        await self._session.close()