import socket
import struct
import binascii

buttons = {
  "Persil": "ac63be5aea19"     
}

last_tid = {}
rawSocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
while True:
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

    for b in buttons.keys():
        if buttons[b] in binascii.hexlify(ethernet_header[1]) and buttons[b] in binascii.hexlify(dhcp_header[11]):
            # filter duplicate presses
            tid = binascii.hexlify(dhcp_header[4])
            if b in last_tid and last_tid[b] == tid:
                continue
            last_tid[b] = tid
            print("%s pressed, TID: %s" % (b, tid))

