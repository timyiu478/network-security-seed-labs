#!/usr/bin/env python3

import fcntl
import struct
import os
import time
from scapy.all import *

TUNSETIFF = 0x400454ca # ioctl command to set interface flags, see linux/if_tun.h
IFF_TUN   = 0x0001
IFF_TAP   = 0x0002
IFF_NO_PI = 0x1000

# Create the tun interface
tun = os.open("/dev/net/tun", os.O_RDWR)
ifr = struct.pack('16sH', b'tim-tun%d', IFF_TUN | IFF_NO_PI) # IFF: interface flags, IFF_NO_PI: no packet info, 16sH: 16-byte string and 2-byte unsigned short = 18 bytes, ifr: interface request
ifname_bytes  = fcntl.ioctl(tun, TUNSETIFF, ifr)

# Get the interface name
ifname = ifname_bytes.decode('UTF-8')[:16].strip("\x00")
print("Interface Name: {}".format(ifname))

# Set the interface IP address and bring it up
os.system("ip addr add 192.168.60.99/24 dev {}".format(ifname)) # need to share the same subnet with the private network
os.system("ip link set dev {} up".format(ifname))

while True:
    # Get a packet from the tun interface
    packet = os.read(tun, 2048)
    if packet:
        ip = IP(packet)
        print(ip.summary())

        # Check if the packet is a ICMP request
        if ip.haslayer(ICMP) and ip[ICMP].type == 8:
            # Construct the ICMP reply packet: Pretend to be the destination IP
            icmp_reply = IP(dst=ip.src, src=ip.dst) / ICMP(type=0, id=ip[ICMP].id, seq=ip[ICMP].seq) / Raw(load=ip[Raw].load)
            os.write(tun, bytes(icmp_reply)) # send the ICMP reply packet back to the sender
