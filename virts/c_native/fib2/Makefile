default:/home/cc/vui/virts/c_native/fib2/boot.asm /home/cc/vui/virts/c_native/fib2/fib2.c
	@mkdir -p /home/cc/vui/virts/c_native/fib2/build
	@nasm -felf64 /home/cc/vui/virts/c_native/fib2/boot.asm -o /home/cc/vui/virts/c_native/fib2/build/boot.o
	@gcc -O3 -nostdlib -c -o /home/cc/vui/virts/c_native/fib2/build/fib2.o /home/cc/vui/virts/c_native/fib2/fib2.c
	@ld -T /home/cc/vui/virts/c_native/fib2/rt.ld -o /home/cc/vui/virts/c_native/fib2/build/fib2.elf /home/cc/vui/virts/c_native/fib2/build/boot.o /home/cc/vui/virts/c_native/fib2/build/fib2.o
	@objcopy -O binary /home/cc/vui/virts/c_native/fib2/build/fib2.elf /home/cc/vui/virts/c_native/fib2/build/fib2.bin