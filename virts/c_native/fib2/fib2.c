#pragma GCC push_options
#pragma GCC optimize ("O0")

int fib2(int n) {
    if (n < 2) return n;
		// this is a hacky way to force gcc to not constant fold
		asm ("");
    return fib2(n-1) + fib2(n-2);
}

#pragma GCC pop_options