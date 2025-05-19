#!/usr/bin/env python3

import fcntl
import struct
import os
import time
import random
from scapy.all import *

TUNSETIFF = 0x400454ca # ioctl command to set interface flags, see linux/if_tun.h
IFF_TUN   = 0x0001
IFF_TAP   = 0x0002
IFF_NO_PI = 0x1000

IP_A = '10.9.0.11'
PORT = 9090


# Create the tun interface
tun = os.open("/dev/net/tun", os.O_RDWR)
ifr = struct.pack('16sH', b'ser-tun%d', IFF_TUN | IFF_NO_PI) # IFF: interface flags, IFF_NO_PI: no packet info, 16sH: 16-byte string and 2-byte unsigned short = 18 bytes, ifr: interface request
ifname_bytes  = fcntl.ioctl(tun, TUNSETIFF, ifr)

# Get the interface name
ifname = ifname_bytes.decode('UTF-8')[:16].strip("\x00")
print("Interface Name: {}".format(ifname))

# Set the interface IP address and bring it up
os.system("ip link set dev {} up".format(ifname))
os.system("ip addr add 192.168.60.22/24 dev {}".format(ifname))
os.system("ip route add 192.168.53.0/24 via 192.168.60.22 dev {}".format(ifname))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP_A, PORT))

udp_tunnel_clients = {}


while True:
    # this will block until at least one interface is ready
    ready, _, _ = select.select([sock, tun], [], [])

    for fd in ready:
        # Response
        if fd is tun:
            # Get a packet from the tun interface
            packet = os.read(tun, 2048)
            pkt = IP(packet)
            print("From tun <==: {} --> {}".format(pkt.src, pkt.dst))
            srcIp, srcPort = udp_tunnel_clients.get(pkt.dst)
            # Send the packet via the tunnel
            sock.sendto(packet, (srcIp, srcPort))

        # Request
        if fd is sock:
            data, (ip, port) = sock.recvfrom(2048)
            pkt = IP(data)
            udp_tunnel_clients[pkt.src] = (ip, port)
            print("Inside: {} --> {}".format(pkt.src, pkt.dst))
            send(pkt)
