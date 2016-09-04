# Amazon Dash Button Fun

## Quick Hack: Observing Traffic

Observing the traffic is the easiest way to play with the dash button. 

When pressing the Dash button, it wakes up and connects to the WiFi. To start the communication with Amazon, it has to first get an IP address from the router using the DHCP protocol. We know that the button was pressed if we see such a packet in the observed traffic that has the dash button's MAC address as sender.

**Advantages**

+ easy
+ no hardware required

**Disadvantages**

+ has to observe the network traffic
+ still connects to Amazon
+ annoying notifications on the phone

## Configuration

1. You just have to activate the Dash button using the Amazon app. You can abort the activation at the point where you have to select a product.

## Getting the MAC address

Run `discover.py` and follow the instructions.

## Listening for button presses

Set the `BUTTON` variable at the top of the `listen.py` file to the button's MAC address. Run `listen.py` as root. 

Everytime the button is pressed, it's MAC address is displayed.
