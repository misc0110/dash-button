# Dash Button Fun
The aim of this project is to make the Amazon Dash button useful (sorry Amazon, but now it is quite useless). To accomplish that, we developed a simple IoT framework that can connect the button to any HTTP or MQTT server.

## About
This repository provides two methods that can be used in three different ways to use any Amazon Dash button for your own purpose. 

* Quick Hack: Observing the traffic
* Dash Endpoint
	* On an openWRT router
	* Using a Raspberry Pi

Furthermore, the project provides a simple Python IoT framework, that allows to publish button presses as HTTP or MQTT messages. It supports all three ways of observing button presses. 

## Listening to the Button

For a quick test, you can try the [traffic observer](observer). This quick hack monitors the network traffic for the dash button's DHCP request. 
If you want to use the button for a real project, I suggest either setting up an [openWRT router](openwrt) or a [Raspberry Pi](rpi) as an endpoint.
(Either click on the links or checkout the README.md in the respective folder)

Both methods provide a Python script (*listen.py*) that allows to test the setup. It can also be used as base for own projecs.

## IoT Framework

We provide a simple IoT framework that builds upon the *listen.py* scripts. The framework provides an abstraction from the used method and can be used with both methods. 

With the framework, a handler can be installed for each buttons. Whenever the button is pressed, either a MQTT or a HTTP message is published. The code is as simple as
```python
from dashiot import DashIoT

# Create an MQTT publisher that uses the network observer for detecting button presses
mqtt = DashIoT(DashIoT.Connector.OBSERVER, DashIoT.Protocol.MQTT)

# If button with mac address "ac63be5aea19" is pressed, send the mac address under the topic "dash/button1"
mqtt.publish_handler("ac63be5aea19", lambda x: ("dash/button1", x))
        
# MQTT server that accepts our messages
mqtt.connect("iot.eclipse.org", 1883)

# Publish all detected button presses forever
mqtt.run()
```

The `DashIoT` constructor takes the connector (either `DashIoT.Connector.OBSERVER` for the traffic observer or `DashIoT.Connector.SERVER` for the endpoint) and the protocol (either `DashIoT.Protocol.MQTT` or `DashIoT.Protocol.HTTP`).
### MQTT
If MQTT is used, the Python package `paho-mqtt` has to be installed (e.g. using `sudo pip install paho-mqtt`). The sample (*test_mqtt.py*) uses Eclipse's public MQTT server ([iot.eclipse.org](http://iot.eclipse.org)). However, any other MQTT server can be used. 

For every button, a handler has to be configured using `publish_handler`. The first argument is the button's MAC address, the second parameter is a callback function that receives the MAC address and returns a tuple of topic and message.

The script *test_view_mqtt.py* is a simple MQTT subscriber that displays the published messages.


### HTTP
If HTTP is used, the framework issues an HTTP GET request to the given URL. As with the MQTT handler, the `publish_handler` function takes the MAC address of the button as the first parameter and a callback funtion as the second parameter. The callback function returns a tuple of GET parameter name and GET parameter value, e.g. if the GET request should be "?msg=data", the callback must return `("msg", "data")`.

A simple HTTP test server can be started using `sudo python -m SimpleHTTPServer 80`.