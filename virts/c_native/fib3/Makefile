default:/home/cc/vui/virts/c_native/fib3/boot.asm /home/cc/vui/virts/c_native/fib3/fib3.c
	@mkdir -p /home/cc/vui/virts/c_native/fib3/build
	@nasm -felf64 /home/cc/vui/virts/c_native/fib3/boot.asm -o /home/cc/vui/virts/c_native/fib3/build/boot.o
	@gcc -O3 -nostdlib -c -o /home/cc/vui/virts/c_native/fib3/build/fib3.o /home/cc/vui/virts/c_native/fib3/fib3.c
	@ld -T /home/cc/vui/virts/c_native/fib3/rt.ld -o /home/cc/vui/virts/c_native/fib3/build/fib3.elf /home/cc/vui/virts/c_native/fib3/build/boot.o /home/cc/vui/virts/c_native/fib3/build/fib3.o
	@objcopy -O binary /home/cc/vui/virts/c_native/fib3/build/fib3.elf /home/cc/vui/virts/c_native/fib3/build/fib3.bin