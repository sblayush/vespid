#include <stdio.h>
#include <wasp/Virtine.h>
#include <wasp/util.h>
#include <memory>
#include <string.h>
#include <wasp/Cache.h>
#include <stdlib.h>
#include <fcntl.h>
#include <wasp/c.h>


unsigned long nanos(void) {
	struct timespec ts;
	clock_gettime(CLOCK_MONOTONIC, &ts);

	return ts.tv_sec * 1000 * 1000 * 1000 + ts.tv_nsec;
}


int main(int argc, char **argv, char* bin_path) {
	FILE *stream = fopen(bin_path, "r");
	if (stream == NULL) return -1;

	fseek(stream, 0, SEEK_END);
	size_t sz = ftell(stream);
	void *bin = malloc(sz);
	fseek(stream, 0, SEEK_SET);
	fread(bin, sz, 1, stream);
	fclose(stream);

	printf("# n, latency\n");
	unsigned long start = nanos();
	wasp_run_virtine((const char *)bin, sz, 0x9000 + (sz & ~0xFFF), &n, sizeof(n), NULL);
	unsigned long end = nanos();
	printf("%d, %5.2f\n", n, (end - start) / 1000.0f);
}
