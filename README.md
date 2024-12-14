rewrite this: 

# HomeAssistant-bang_olufsen_halo
This is a HomeAssistant Integration for the Bang & Olufsen Beoremote Halo.

Installation:

1. Copy the Contents to your Home Assistant custom_components folder.

Usage:

1. The Integration should detect your Beoremote Halo via mDNS, if not you can add one manually through the integration.

2. When configuring the Halo, you will have the option to provide a JSON configuration for the pages & buttons.

Please see https://bang-olufsen.github.io/beoremote-halo/ for an example.

Events:

The integration works via the HomeAssistant EventBus, there are two event types

bang_olufsen_halo_websocket_event_in - For events reported from Beoremote Halo

bang_olugsen_halo_websocket_event_out - For events reported to Beoremote Halo

Sending Events to Halo:

The events sent to Beoremote Halo are sent in YAML format via the bang_olufsen_halo_websocket_event_out Event Type and are serialised in JSON, the serial number of the halo must also be provided.

Example: Sending a Notification

update:<br>
  type: notification</ br>
  id: 497f6eca-6276-4993-bfeb-53cbbbba6f69</ br>
  title: Testing</ br>
  subtitle: This is a test notification</ br>
serial: "1234567"</ br>

Example: Updating a state and subtitle on a button

update:
  type: button
  id: 497f6eca-6276-4993-bfeb-53cbbbba6f03
  state: active
  subtitle: "On"
serial: "1234567"

Please see https://bang-olufsen.github.io/beoremote-halo/ for more examples

Receiving Events from Halo:

The events received from Beoremote Halo are received in YAML format via the bang_olufsen_halo_websocket_event_in Event Type, the Serial Number of the halo is provided.

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

I have given you the tool, the only limit now is your imagination :)


