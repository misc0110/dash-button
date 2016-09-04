# Dash Button Fun

## Standalone: Raspberry Pi

We will configure a Raspberry Pi to act as access point for the dash button. Similar to the openWRT solution, this gives us full control over the button's communication. 

## Configuration

1. Install Raspbian Jessie Lite.
2. Install required packages `sudo apt-get install hostapd dnsmasq isc-dhcp-server` 
3. Get a WiFi adapter that is compatible with the Raspberry Pi. I used a [Netgear WNA1000M N150 Micro Adapter](https://www.amazon.de/Netgear-WNA1000M-100FRS-WL-USB-WNA1000M-100GRS-150MBit/dp/B004URO9FG/). It has a Realtek RTL8192CU chipset. If your chipset is supported out-of-the-box, skip the next step.
4. Install the modified hostapd version from Realtek. Either take the binary [`hostapd`](hostapd) from this repository, or follow these steps to build it yourself.
	+ Download the RTL8192CU driver from Realtek: [http://www.realtek.com/downloads/downloadsView.aspx?Langid=1&PNid=21&PFid=48&Level=5&Conn=4&DownTypeID=3&GetDown=false&Downloads=true#2772](http://www.realtek.com/downloads/downloadsView.aspx?Langid=1&PNid=21&PFid=48&Level=5&Conn=4&DownTypeID=3&GetDown=false&Downloads=true#2772)
	+ Navigate to *RTL8188C_8192C_USB_linux_v4.0.2_9000.20130911/wpa_supplicant_hostapd/* and extract *wpa_supplicant_hostapd-0.8_rtw_r7475.20130812.tar.gz*
	+ navigate to *wpa_supplicant_hostapd-0.8_rtw_r7475.20130812/hostapd/* and build with `make`.
	+ remove the installed *hostapd* binary `sudo mv /usr/sbin/hostapd /usr/sbin/hostapd.orig`
	+ install the new *hostapd* binary `sudo cp hostapd /usr/sbin/hostapd`
5. Configure *hostapd* by creating the file */etc/hostapd/hostapd.conf* with the following contents (if you don't have the RTL8192CU chipset, replace `rtl871xdrv` with `nl80211`)

        interface=wlan0
        driver=rtl871xdrv
        ssid=DashIoT
        channel=1
        auth_algs=1
        wmm_enabled=0
        wpa=1
        wpa_passphrase=yourpassword
        wpa_key_mgmt=WPA-PSK
        wpa_pairwise=CCMP
        macaddr_acl=0

6. Configure the WiFi adapter in */etc/network/interfaces* to use the 192.168.50.x network. It should look like this

        auto lo
        iface lo inet loopback
        
        iface eth0 inet manual
        
        iface wlan0 inet static
            address 192.168.50.1
            netmask 255.255.255.0
        
        hostapd /etc/hostapd/hostapd.conf

7. Configure the DHCP server in */etc/dhcp/dhcp.conf*. It should look like this

        default-lease-time 600;
        max-lease-time 7200;
        option routers 192.168.50.1;
        option domain-name-servers 192.168.50.1, 192.168.50.1;

        subnet 192.168.50.0 netmask 255.255.255.0 {
                pool {
                        max-lease-time 600;
                        range 192.168.50.10 192.168.50.50;
                        option routers 192.168.50.1;
                        option domain-name-servers 192.168.50.1, 192.168.50.1;
                        allow unknown-clients;
                }
        }
        
8. Enable NAT:

        sudo sysctl -w net.ipv4.ip_forward=1

        sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
        sudo iptables -A FORWARD -i eth0 -o wlan0 -j ACCEPT
        sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT

9. Reboot the Raspberry Pi (`sudo reboot`)
10. Test whether the access point works by running `sudo hostapd /etc/hostapd/hostapd.conf`. You should be able to connect to the access point with any wireless device.
11. Activate your Dash button using the Amazon app. You can abort the activation at the point where you have to select a product.
12. Redirect the Amazon endpoint to the Raspberry Pi by adding the following line to */etc/dnsmasq.conf*:

        address=/parker-gw-eu.amazon.com/192.168.50.1

13. Restart *dnsmasq*: `sudo service dnsmasq restart`
## Listening for button presses

All the tools from the openWRT setup also work with the Raspberry Pi setup. Just run `sudo python openwrt/listen.py` to test the setup. Every time the button is pressed, the MAC address of the button is displayed.
 
