#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include "virtine.h"
#include <stdio.h>
#include <sys/types.h>
#include "multiply.h"


#pragma GCC push_options
#pragma GCC optimize ("O0")

virtine int multiply(int a, int b){
return a*b;
}

#pragma GCC pop_options
