#include <stdio.h>
#include <stdlib.h>
#include "####vname####.h"

int main(int argc, char **argv) {
	int arg1 = atoi(argv[1]);
	int arg2 = atoi(argv[2]);
	int res = ####vname####(arg1, arg2);
	printf("%d", res);
}
