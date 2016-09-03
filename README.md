# Dash Button Fun
Making the Amazon Dash button useful.

## About
This repository provides.... **TODO**

## Quick Hack: Observing Traffic

The following method is a very easy way to execute custom commands on a button press.

**Advantages**

+ easy
+ no hardware required

**Disadvantages**

+ has to observe the network traffic
+ still connects to Amazon
+ annoying notifications on the phone

### Idea

When pressing the Dash button, it wakes up and connects to the WiFi. To start the communication with Amazon, it has to first get an IP address from the router using the DHCP protocol. We know that the button was pressed if we see such a packet in the observed traffic that has the dash button's MAC address as sender.

### Solution

see folder [observer](observer).


## Easy Solution: OpenWRT Router

If you have a router running openWRT, only a few modifications are required to use the dash button without connection to Amazon.

**Advantages**

+ easy setup
+ does not connect to Amazon

**Disadvantages**

+ router with custom firmware required

### Idea

After the button has its IP address, it starts to resolve `parker-gw-eu.amazon.com`. By sending a fake DNS-entry, we can redirect the communication to our own server. 

### Solution

see folder [openwrt](openwrt).

## Standalone: Raspberry Pi

Using a Raspberry Pi, a standalone IoT infrastructure can be created.

**Advantages**

+ no dependencies
+ no connection to Amazon
+ no router modifications needed

**Disadvantages**

+ requires hardware (RPi + WiFi Dongle)

### Idea

The idea is the same as with the openWRT Router. However, this time we build our own router using a Raspberry Pi.

### Solution

see folder [rpi](rpi).

 