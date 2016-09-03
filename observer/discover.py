import socket
import struct
import binascii
import time

runs = 3
tolerance = 0

filtered = []
rawSocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))

while len(filtered) != 1:
    print("[!] Prepare to press the button in 3 seconds")
    time.sleep(1)
    print("[!] 2...")
    time.sleep(1)
    print("[!] 1...")
    time.sleep(1)
    
    filtered = []
    candidates = []
    
    for i in range(runs):
        print("[!] Press the button...\n")
        t_end = time.time() + 12

        macs = []
        while time.time() < t_end:
            packet = rawSocket.recvfrom(2048)
            ethernet_header = struct.unpack("!6s6s2s", packet[0][0:14])
            
            if ethernet_header[2] != '\x08\00':
                continue # not ip
            
            ip_header = struct.unpack("!1s1s2s2s1s1s1s1s2s4s4s", packet[0][14:34])
            
            if ip_header[7] != '\x11':
                continue # not udp

            if len(packet[0][42:]) < 240:
                continue # not dhcp
            
            dhcp_header = struct.unpack("!1s1s1s1s4s2s2s4s4s4s4s6s10s64s128s4s", packet[0][42:282])

            macs.append(binascii.hexlify(dhcp_header[11]))
        candidates.append(set(macs))
        macs = []

    macs = {}

    for run in range(len(candidates)):
        for mac in candidates[run]:
            if mac in macs: 
                macs[mac] += 1
            else:
                macs[mac] = 1
            
    for m in macs:
        if macs[m] >= len(candidates) - tolerance:
            filtered.append(m)

print("[!] Discovered button with MAC %s" % (filtered[0]))
