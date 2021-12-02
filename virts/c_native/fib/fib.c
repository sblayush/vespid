#pragma GCC push_options
#pragma GCC optimize ("O0")

int fib(int n) {
    if (n < 2) return 1;
    return fib(n-1) + fib(n-2);
}

#pragma GCC pop_options