# Network Security Seed Labs

## About

The SEED project started in 2002 by Wenliang Du, a professor at the Syracuse University. It was funded by a total of 1.3 million dollars from the US National Science Foundation (NSF). This repository contains the notes of the network security labs.

## Notes

| Lab Name | Description |  Notes |
| ---      | --- | ---   |
| VPN Tunneling | Build a simple VPN program using TUN/TAP interface | [README](./labs/VPN_Tunnel/README.md), [DEMO](https://github.com/timyiu478/network-security-seed-labs/blob/main/labs/VPN_Tunnel/README.md#demo)|
| TCP SYN Flooding Attack | Denied of Service Attack on the Web Server via TCP SYN Flooding | [README](./labs/TCP_Attacks/README.md), [DEMO](https://github.com/timyiu478/network-security-seed-labs/blob/main/labs/TCP_Attacks/DEMO.md#tcp-syn-flood-attack-for-denied-of-service-attack)|
| Morris Worm | Write a simple internet worm, test it in an internet simulator | [README](./labs/Morris_Worm/README.md), [DEMO]() |


## Related to Containers

We will use the following rule when assigning docker images to containers and 
when configuring containers:

- A container should use the ```host``` mode if sniffing is needed
- A container should use the ```privileged``` mode if it needs to 

set kernel variables using ```sysctl```
