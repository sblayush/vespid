#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <sys/types.h>
#include "../virtine.h"


#pragma GCC push_options
#pragma GCC optimize ("O0")

virtine ####vcode####

#pragma GCC pop_options


int main(int argc, char **argv) {
####plistdef####
	int res = ####vname####(####plistargs####);
	printf("%d", res);
}
