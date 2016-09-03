# Dash Button Fun

## Easy Solution: OpenWRT Router

## Configuration

+ Edit `/etc/config/dhcp`, add the following line in the `config dnsmasq` section:
`list address '/parker-gw-eu.amazon.com/192.168.1.10'`
+ Restart dnsmasq: `/etc/init.d/dnsmasq restart`

## Listening for button presses

Run `listen.py`.
