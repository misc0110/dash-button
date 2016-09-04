# Dash Button Fun

## Dash Endpoint: OpenWRT Router

If you have a router running openWRT, only a few modifications are required to use it as endpoint for the Dash button. A custom endpoint prevents the button from connecting to Amazon.

After the button has its IP address, it starts to resolve `parker-gw-eu.amazon.com`. By sending a fake DNS-entry, we can redirect the communication to our own server. 

**Advantages**

+ easy setup
+ does not connect to Amazon

**Disadvantages**

+ router with custom firmware required

## Configuration

1. Activate your Dash button using the Amazon app. You can abort the activation at the point where you have to select a product.
2. Edit */etc/config/dhcp*, add the following line in the `config dnsmasq` section:

        list address '/parker-gw-eu.amazon.com/192.168.1.10`
Here, `192.168.1.10` is the IP address of our Dash endpoint. This can be either a local IP or any IP address on the internet.

3. Restart dnsmasq: `/etc/init.d/dnsmasq restart`

## Listening for button presses

Run the `listen.py` script as your Dash endpoint on the server specified in */etc/config/dhcp*. In this example this would be a local computer with the IP  `192.168.1.10`. 

Everytime the button is pressed, it connects to our endpoint. The script outputs the button's MAC address on every press.
