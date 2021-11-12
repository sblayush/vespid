#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include "virtine.h"
#include <stdio.h>
#include <sys/types.h>


#pragma GCC push_options
#pragma GCC optimize ("O0")

virtine int add(int a, int b){
return a+b;
}

#pragma GCC pop_options


int main(int argc, char **argv) {
	int arg1 = atoi(argv[1]);
	int arg2 = atoi(argv[2]);
	int res = add(arg1, arg2);
	printf("%d", res);
}
