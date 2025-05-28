# Seed Labs

## About

The SEED project started in 2002 by Wenliang Du, a professor at the Syracuse University. It was funded by a total of 1.3 million dollars from the US National Science Foundation (NSF). This repository contains the notes of the security labs.

## Notes

| Lab Name | Description |  Notes |
| ---      | --- | ---   |
| VPN Tunneling | Build a simple VPN program using TUN/TAP interface | [README](./labs/VPN_Tunnel/README.md), [DEMO](https://github.com/timyiu478/network-security-seed-labs/blob/main/labs/VPN_Tunnel/README.md#demo)|
| TCP SYN Flooding Attack | Denied of Service Attack on the Web Server via TCP SYN Flooding | [README](./labs/TCP_Attacks/README.md), [DEMO](https://github.com/timyiu478/network-security-seed-labs/blob/main/labs/TCP_Attacks/DEMO.md#tcp-syn-flood-attack-for-denied-of-service-attack)|
| Morris Worm - Buffer Over Flow Attack | Inject shell code by exploiting the buffer overflow vulnerability | [README](./labs/Morris_Worm/README.md#task-1-attack-the-first-target), [DEMO](https://github.com/timyiu478/network-security-seed-labs/blob/main/labs/Morris_Worm/README.md#demo) |
| Race Condition and SET-UID Vulnerabilities | Exploit race condition and SET-UID vulnerabilities for privileged esculation | [README](./labs/Race_Condition/README.md), [DEMO](https://github.com/timyiu478/seed-labs/blob/main/labs/Race_Condition/README.md#demo) |
| Morris Worm - Self Duplication and Propagation | Write a simple internet worm and test it in internet emulator | [README](./labs/Morris_Worm/README.md#step-3-self-duplication), [DEMO](https://github.com/timyiu478/seed-labs/blob/main/labs/Morris_Worm/README.md#morris-worm-demo) |
| Spectre Attack | Exploit CPU mechanism about out of order execution, branch prediction, and caching to access unauthorised memory region | [README](./labs/Spectre_Attack/README.md) |
| DNS Rebinding Attack | Use DNS Rebinding technique to bypass the browser same origin policy | [README](./labs/DNS_Rebinding/README.md), [DEMO](https://github.com/timyiu478/seed-labs/blob/main/labs/DNS_Rebinding/README.md#demo) |


## Related to Containers

We will use the following rule when assigning docker images to containers and 
when configuring containers:

- A container should use the ```host``` mode if sniffing is needed
- A container should use the ```privileged``` mode if it needs to 

set kernel variables using ```sysctl```
