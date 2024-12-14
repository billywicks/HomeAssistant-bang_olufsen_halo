<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>

<h1>HomeAssistant Bang & Olufsen Beoremote Halo Integration</h1>
<p>This is a custom Home Assistant integration for the <b>Bang & Olufsen Beoremote Halo</b>, enabling full interaction through Home Assistant’s Event Bus.</p>

<hr>

<h2>Installation</h2>
<ol>
    <li>Copy the contents of this repository into the <code>custom_components</code> folder of your Home Assistant installation.</li>
</ol>

<hr>

<h2>Usage</h2>
<ol>
    <li><b>Automatic Device Discovery:</b>
        <ul>
            <li>The integration should detect your Beoremote Halo using <b>mDNS</b>.</li>
            <li>If the device is not detected automatically, you can manually add it through the Home Assistant Integrations menu.</li>
        </ul>
    </li>
    <li><b>Device Configuration:</b>
        <ul>
            <li>During setup, you will have the option to provide a custom <b>JSON configuration</b> for pages and buttons.</li>
        </ul>
    </li>
</ol>

<h3>Example: Button/Page Configuration</h3>
<pre><code>{
  "configuration": {
    "version": "1.0.1",
    "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
    "pages": [
      {
        "title": "Page Title",
        "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
        "buttons": [
          {
            "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
            "title": "Button Title",
            "subtitle": "Subtitle",
            "value": 100,
            "state": "active",
            "content": {
              "text": "string"
            },
            "default": true
          }
        ]
      }
    ]
  }
}
</code></pre>

<p>👉 Refer to the <a href="https://bang-olufsen.github.io/beoremote-halo/">Beoremote Halo Configuration Guide</a> for examples and usage details.</p>

<hr>

<h2>Events</h2>
<p>The integration works through the Home Assistant <b>Event Bus</b> using two event types:</p>
<ul>
    <li><b><code>bang_olufsen_halo_websocket_event_in</code></b> - Events reported <b>from</b> the Beoremote Halo.</li>
    <li><b><code>bang_olufsen_halo_websocket_event_out</code></b> - Events sent <b>to</b> the Beoremote Halo.</li>
</ul>

<hr>

<h2>Sending Events to the Beoremote Halo</h2>
<p>Events sent <b>to</b> the Beoremote Halo are serialized into <b>JSON</b> and must be sent as <b>YAML</b> using the <code>bang_olufsen_halo_websocket_event_out</code> event type.  
The <b>serial number</b> of the device <b>must</b> be included in the payload.</p>

<h3>Example 1: Sending a Notification</h3>
<pre><code>update:
  type: notification
  id: 497f6eca-6276-4993-bfeb-53cbbbba6f69
  title: "Testing"
  subtitle: "This is a test notification"
serial: "1234567"
</code></pre>

<h3>Example 2: Updating a Button's State and Subtitle</h3>
<pre><code>update:
  type: button
  id: 497f6eca-6276-4993-bfeb-53cbbbba6f03
  state: active
  subtitle: "On"
serial: "1234567"
</code></pre>

<p>👉 For more examples, see the <a href="https://bang-olufsen.github.io/beoremote-halo/">Beoremote Halo Documentation</a>.</p>

<hr>

<h2>Receiving Events from the Beoremote Halo</h2>
<p>Events received <b>from</b> the Beoremote Halo are sent through the <code>bang_olufsen_halo_websocket_event_in</code> event type.  
Each event includes the <b>serial number</b> of the reporting device.</p>

<h3>Example: Received Event Data</h3>
<pre><code>event_type: bang_olufsen_halo_websocket_event_in
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
</code></pre>

<hr>

<h2>Unleash Your Creativity!</h2>
<p>With this integration, the only limit is your imagination. 🚀 Create custom automations, notifications, and controls that connect seamlessly with your Beoremote Halo!</p>

</body>
</html>
