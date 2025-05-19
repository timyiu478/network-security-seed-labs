# Network Security Seed Labs

## About

The SEED project started in 2002 by Wenliang Du, a professor at the Syracuse University. It was funded by a total of 1.3 million dollars from the US National Science Foundation (NSF). This repository contains the notes of its network security labs.

## Notes

### Done

| Lab Name | Status |  Notes |
| ---      | ---    |  ---   |

### TODO

| Lab Name | Status |  Notes |
| ---      | ---    |  ---   |
| Sniffing/Spoofing   | TODO | [README](./labs/Sniffing_Spoofing/README.md)|
| ARP Cache Poisoning | TODO | [README](./labs/ARP_Attack/README.md)|
| IP/ICMP             | TODO | [README](./labs/IP_Attacks/README.md)| 
| TCP Attacks         | TODO | [README](./labs/TCP_Attacks/README.md)|
| Mitnick Attack      | TODO | [README](./labs/Mitnick_Attack/README.md)| 
| Local DNS Attack    | TODO | [README](./labs/DNS_Local/README.md)|
| Remote DNS Attack   | TODO | [README](./labs/DNS_Remote/README.md)|
| DNS Rebinding Attack| TODO | [README](./labs/DNS_Rebinding/README.md)|
| DNS-in-a-box         | TODO | [README](./labs/DNS_in_a_Box/README.md) |
| Firewall Lab        | TODO | [README](./labs/Firewall/README.md)|
| VPN Tunneling       | TODO | [README](./labs/VPN_Tunnel/README.md) |
| VPN Lab             | TODO | [README](./labs/VPN/README.md)|
| BGP Lab              | TODO | [README](./labs/BGP_Basic/README.md)|

## Related to Containers

We will use the following rule when assigning docker images to containers and 
when configuring containers:

- A container should use the ```host``` mode if sniffing is needed
- A container should use the ```privileged``` mode if it needs to 

set kernel variables using ```sysctl```
