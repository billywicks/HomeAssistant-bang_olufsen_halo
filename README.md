HomeAssistant Bang & Olufsen Beoremote Halo Integration

This is a Home Assistant custom integration for the Bang & Olufsen Beoremote Halo, enabling seamless interaction through Home Assistant’s event system.

Installation
	1.	Copy the contents of this repository into the custom_components folder of your Home Assistant installation.

Usage
	1.	Automatic Device Discovery:
	The integration automatically detects your Beoremote Halo using mDNS.
	If detection fails, you can manually add the device through the Home Assistant Integrations menu.
	2.	Configuration:
	During setup, you have the option to provide a custom JSON configuration for pages and buttons on the Beoremote Halo.
	Refer to the official documentation for configuration examples:
  [Bang & Olufsen Beoremote Halo Configuration Guide](https://bang-olufsen.github.io/beoremote-halo/)

Events

The integration works through the Home Assistant Event Bus using two event types:
	1.	bang_olufsen_halo_websocket_event_in - Events reported from the Beoremote Halo.
	2.	bang_olufsen_halo_websocket_event_out - Events sent to the Beoremote Halo.

Sending Events to the Beoremote Halo

To send events to the Beoremote Halo, use the bang_olufsen_halo_websocket_event_out event type.
Events must be formatted in YAML and are automatically serialized to JSON.
Include the serial number of your device in the payload.

Example 1: Sending a Notification

update:
  type: notification
  id: 497f6eca-6276-4993-bfeb-53cbbbba6f69
  title: "Testing"
  subtitle: "This is a test notification"
serial: "1234567"

Example 2: Updating Button State and Subtitle

update:
  type: button
  id: 497f6eca-6276-4993-bfeb-53cbbbba6f03
  state: active
  subtitle: "On"
serial: "1234567"

For additional examples, refer to the Beoremote Halo Documentation.

Receiving Events from the Beoremote Halo

Events from the Beoremote Halo are received through the bang_olufsen_halo_websocket_event_in event type. Each event contains the serial number of the reporting device.

Example: Received Event Data

event_type: bang_olufsen_halo_websocket_event_in
data:
  event:
    type: power
    capacity: 100
    state: discharging
  serial: "1234567"
origin: LOCAL
time_fired: "2024-12-14T22:03:01.304157+00:00"
context:
  id: 01JF3K4HSRX7MQP1XRP08CZQ87
  parent_id: null
  user_id: null

You now have the tools at your fingertips—let your creativity run wild! 😊
