<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HomeAssistant-bang_olufsen_halo</title>
</head>
<body>
    <h1>HomeAssistant-bang_olufsen_halo</h1>

    <p>This is a Home Assistant Integration for the Bang & Olufsen Beoremote Halo.</p>

    <hr>

    <h2>Installation:</h2>
    <ol>
        <li>Copy the contents to your Home Assistant <code>custom_components</code> folder.</li>
    </ol>

    <hr>

    <h2>Usage:</h2>
    <ol>
        <li>The integration should detect your Beoremote Halo via mDNS. If not, you can add one manually through the integration setup.</li>
        <li>When configuring the Halo, you will have the option to provide a JSON configuration for pages and buttons.</li>
    </ol>

    <p>For more examples and configuration details, please visit:  
        <a href="https://bang-olufsen.github.io/beoremote-halo/">Bang & Olufsen Beoremote Halo Documentation</a>
    </p>

    <hr>

    <h2>Events:</h2>
    <p>The integration works via the Home Assistant EventBus, supporting two event types:</p>
    <ul>
        <li><code>bang_olufsen_halo_websocket_event_in</code> – Events received from Beoremote Halo</li>
        <li><code>bang_olufsen_halo_websocket_event_out</code> – Events sent to Beoremote Halo</li>
    </ul>

    <hr>

    <h2>Sending Events to Halo:</h2>
    <p>Send events using YAML format via <code>bang_olufsen_halo_websocket_event_out</code>. The serial number of the Halo must be provided.</p>

    <h3>Example: Sending a Notification</h3>
    <pre>
<code>
update:
  type: notification
  id: 497f6eca-6276-4993-bfeb-53cbbbba6f69
  title: Testing
  subtitle: This is a test notification
serial: "1234567"
</code>
    </pre>

    <h3>Example: Updating a Button State</h3>
    <pre>
<code>
update:
  type: button
  id: 497f6eca-6276-4993-bfeb-53cbbbba6f03
  state: active
  subtitle: "On"
serial: "1234567"
</code>
    </pre>

    <hr>

    <h2>Receiving Events from Halo:</h2>
    <p>Events received from Beoremote Halo are in YAML format using the <code>bang_olufsen_halo_websocket_event_in</code> event type, including the Halo's serial number.</p>

    <pre>
<code>
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
</code>
    </pre>

    <hr>

    <h2>Support & Donations 💖</h2>
    <p>If you enjoy using this integration and would like to support its development, consider making a donation. Every contribution helps keep the project going!</p>

    <p><a href="https://paypal.me/BillyMartinWicks" target="_blank"><strong>Donate via PayPal</strong></a></p>

    <p>Thank you for your support! 😊</p>

    <hr>

    <p>Happy Automating! 🚀</p>
    <p><em>I have given you the tool; the only limit now is your imagination!</em></p>
</body>
</html>
