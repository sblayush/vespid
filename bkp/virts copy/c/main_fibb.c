#include <stdio.h>
#include <stdlib.h>
#include "fibb.h"

int main(int argc, char **argv) {
	int arg1 = atoi(argv[1]);
	int arg2 = atoi(argv[2]);
	int res = fibb(arg1, arg2);
	printf("%d", res);
}
