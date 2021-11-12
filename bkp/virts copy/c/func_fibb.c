#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include "virtine.h"
#include <stdio.h>
#include <sys/types.h>
#include "fibb.h"


#pragma GCC push_options
#pragma GCC optimize ("O0")

virtine int fibb(int a, int b){
if(a<1){
return 1;
}
return a*fibb(a-1, b);
}

#pragma GCC pop_options
