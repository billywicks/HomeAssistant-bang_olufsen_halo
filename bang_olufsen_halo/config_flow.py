import json
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.components.zeroconf import ZeroconfServiceInfo
from .const import DOMAIN

CONF_JSON_DATA = "json_data"

class MyDeviceConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle a manual configuration via user input."""
        if user_input is not None:
            # Store host and port in context, proceed to JSON step
            self.context["user_data"] = user_input
            return await self.async_step_configure_json()

        schema = vol.Schema({
            vol.Required(CONF_HOST): str,
            vol.Required(CONF_PORT, default=8080): int,
            vol.Required(CONF_JSON_DATA): str
        })
        return self.async_show_form(step_id="user", data_schema=schema)

    async def async_step_zeroconf(self, discovery_info: ZeroconfServiceInfo):
        """Handle a discovered device via mDNS/zeroconf."""
        host = discovery_info.host
        port = discovery_info.port
        serial = discovery_info.properties.get("serial")

        # Use the serial as the unique ID if available; otherwise fallback to host
        unique_id = serial if serial else host
        await self.async_set_unique_id(unique_id)
        self._abort_if_unique_id_configured()

        # Store the discovered data in context
        self.context["user_data"] = {
            CONF_HOST: host,
            CONF_PORT: port,
            "serial": serial
        }

        # Move to the JSON configuration step
        return await self.async_step_configure_json()

    async def async_step_configure_json(self, user_input=None):
        """A step to get JSON data that will be sent to the device."""
        if user_input is not None:
            # Combine previously collected data with the JSON data
            data = dict(self.context["user_data"])
            data[CONF_JSON_DATA] = user_input[CONF_JSON_DATA]
            return self.async_create_entry(
                title=data.get("serial") or data[CONF_HOST],
                data=data
            )

        schema = vol.Schema({
            vol.Required(CONF_JSON_DATA): str
        })
        return self.async_show_form(step_id="configure_json", data_schema=schema)