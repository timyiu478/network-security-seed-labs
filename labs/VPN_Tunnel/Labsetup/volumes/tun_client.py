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

SERVER_IP = '10.9.0.11' # VPN server IP
SERVER_PORT = 9090 # VPN server port

# Create the tun interface
tun = os.open("/dev/net/tun", os.O_RDWR)
ifr = struct.pack('16sH', b'tim-tun%d', IFF_TUN | IFF_NO_PI) # IFF: interface flags, IFF_NO_PI: no packet info, 16sH: 16-byte string and 2-byte unsigned short = 18 bytes, ifr: interface request
ifname_bytes  = fcntl.ioctl(tun, TUNSETIFF, ifr)

# Get the interface name
ifname = ifname_bytes.decode('UTF-8')[:16].strip("\x00")
print("Interface Name: {}".format(ifname))

# Set the interface IP address and bring it up
os.system("ip link set dev {} up".format(ifname))
os.system("ip addr add 192.168.53.99/24 dev {}".format(ifname))
os.system("ip route add 192.168.60.0/24 dev {} via 192.168.53.99".format(ifname))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    # this will block until at least one interface is ready
    ready, _, _ = select.select([sock, tun], [], [])

    for fd in ready:
        # Client Request
        if fd is tun:
            # Get a packet from the tun interface
            packet = os.read(tun, 2048)
            pkt = IP(packet)
            print("From tun ==>: {} --> {}".format(pkt.src, pkt.dst))
            # Send the packet via the tunnel
            sock.sendto(packet, (SERVER_IP, SERVER_PORT))

        # Client Response
        if fd is sock:
            # Get a packet from the tun interface
            data, (ip, port) = sock.recvfrom(2048)
            pkt = IP(data)
            print("Inside: {} --> {}".format(pkt.src, pkt.dst))
            os.write(tun, data)
