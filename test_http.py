from dashiot import DashIoT

# Create an HTTP publisher that uses the network observer for detecting button presses
http = DashIoT(DashIoT.Connector.OBSERVER, DashIoT.Protocol.HTTP)

# If button with mac address "ac63be5aea19" is pressed, send the mac address as parameter "btn"
http.publish_handler("ac63be5aea19", lambda x: ("btn", x))

# HTTP server to which we want to publish
http.connect("http://localhost:8080/")

# Publish all detected button presses forever
http.run()

