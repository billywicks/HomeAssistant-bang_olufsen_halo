import logging
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import PERCENTAGE
from homeassistant.core import callback
from .const import DOMAIN, EVENT_TYPE_IN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    ws_client = hass.data[DOMAIN].get(config_entry.entry_id)

    if not ws_client:
        _LOGGER.error("WebSocket client not found for sensor setup")
        return False

    motion_sensor = BeoremoteHaloMotionSensor(ws_client)
    battery_sensor = BeoremoteHaloBatterySensor(ws_client)
    async_add_entities([motion_sensor, battery_sensor], True)

    # Register event listener
    async def handle_event(event):
        await motion_sensor.async_event_received(event.data)
        await battery_sensor.async_event_received(event.data)

    hass.bus.async_listen(EVENT_TYPE_IN, handle_event)
    _LOGGER.info("Binary and Battery sensor setup complete")


# Motion Sensor Class
class BeoremoteHaloMotionSensor(BinarySensorEntity):
    def __init__(self, ws_client):
        self._ws_client = ws_client
        self._attr_name = f"Beoremote Halo Motion Sensor {ws_client.serial}"
        self._attr_is_on = False
        self._attr_device_class = "motion"
        self._attr_unique_id = f"bang_olufsen_halo_motion_sensor_{ws_client.serial}"

    @property
    def is_on(self):
        """Return true if motion is detected."""
        return self._attr_is_on

    @callback
    async def async_event_received(self, event_data):
        """Handle received event."""
        event_type = event_data.get("event", {}).get("type")
        event_state = event_data.get("event", {}).get("state")
        event_serial = event_data.get("serial")

        if event_serial == self._ws_client.serial and event_type == "system":
            self._attr_is_on = event_state == "active"

            _LOGGER.info(
                "Motion sensor state updated to %s for serial %s", 
                self._attr_is_on, 
                event_serial
            )
            self.async_write_ha_state()


# Battery Sensor Class
class BeoremoteHaloBatterySensor(SensorEntity):
    """Representation of the Beoremote Halo Battery Sensor."""

    def __init__(self, ws_client):
        self._ws_client = ws_client
        self._attr_name = f"Beoremote Halo Battery {ws_client.serial}"
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_native_value = 0
        self._attr_device_class = "battery"
        self._attr_unique_id = f"bang_olufsen_halo_battery_sensor_{ws_client.serial}"
        self._charging = False

    @property
    def extra_state_attributes(self):
        """Return extra attributes."""
        return {
            "charging": self._charging
        }

    @callback
    async def async_event_received(self, event_data):
        """Handle received event."""
        event_type = event_data.get("event", {}).get("type")
        event_capacity = event_data.get("event", {}).get("capacity")
        event_state = event_data.get("event", {}).get("state")
        event_serial = event_data.get("serial")

        if event_serial == self._ws_client.serial and event_type == "power":
            if isinstance(event_capacity, int):
                self._attr_native_value = event_capacity
            else:
                _LOGGER.warning("Invalid capacity received: %s", event_capacity)

            self._charging = event_state == "charging"

            _LOGGER.info(
                "Battery state updated: %d%%, Charging: %s for serial %s",
                self._attr_native_value, self._charging, event_serial
            )
            self.async_write_ha_state()