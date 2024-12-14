import asyncio
import json
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_HOST, CONF_PORT
from .const import DOMAIN, EVENT_TYPE_OUT
from .websocket_client import MyDeviceWebSocketClient

_LOGGER = logging.getLogger(__name__)

PLATFORMS = []
CONF_JSON_DATA = "json_data"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    host = entry.data[CONF_HOST]
    port = entry.data[CONF_PORT]
    serial = entry.data.get("serial")
    json_str = entry.data.get(CONF_JSON_DATA)

    # Create a websocket client instance with serial
    ws_client = MyDeviceWebSocketClient(hass, host, port, serial)
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = ws_client

    # Connect to the device WebSocket
    await ws_client.connect()
    ws_client.start_listening()

    # If user provided JSON, parse and send it to the device
    if json_str:
        try:
            json_data = json.loads(json_str)
            await ws_client.send_message(json_data)
            _LOGGER.debug("Sent JSON data to device: %s", json_data)
        except json.JSONDecodeError:
            _LOGGER.error("Invalid JSON provided in config, could not send")

    # Setup entity platforms if needed
    for platform in PLATFORMS:
        hass.async_add_job(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    # Register the event listener only once for this domain
    if "event_registered" not in hass.data[DOMAIN]:
        async def async_bang_olufsen_halo_websocket_event_handler(event):
            event_serial = event.data.get("serial")
            if not event_serial:
                _LOGGER.warning("Event missing 'serial'; cannot route message.")
                return

            ws_client_target = None
            for obj in hass.data[DOMAIN].values():
                if isinstance(obj, MyDeviceWebSocketClient) and obj.serial == event_serial:
                    ws_client_target = obj
                    break

            if not ws_client_target:
                _LOGGER.warning("No WebSocket client found for serial %s", event_serial)
                return

            _LOGGER.debug("Sending event data to device %s: %s", event_serial, event.data)
            await ws_client_target.send_message(event.data)

        hass.bus.async_listen(EVENT_TYPE_OUT, async_bang_olufsen_halo_websocket_event_handler)
        hass.data[DOMAIN]["event_registered"] = True

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    ws_client = hass.data[DOMAIN].pop(entry.entry_id)
    await ws_client.disconnect()

    results = await asyncio.gather(
        *[hass.config_entries.async_forward_entry_unload(entry, p) for p in PLATFORMS],
        return_exceptions=True
    )
    return all(r is True for r in results)