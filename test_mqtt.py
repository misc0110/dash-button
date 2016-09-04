from dashiot import DashIoT

# Create an MQTT publisher that uses the network observer for detecting button presses
mqtt = DashIoT(DashIoT.Connector.OBSERVER, DashIoT.Protocol.MQTT)

# If button with mac address "ac63be5aea19" is pressed, send the mac address as under the topic "dash/button1"
mqtt.publish_handler("ac63be5aea19", lambda x: ("dash/button1", x))

# MQTT server that accepts our messages
mqtt.connect("iot.eclipse.org", 1883)

# Publish all detected button presses forever
mqtt.run()

