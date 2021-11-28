default:/home/cc/vui/virts/c_native/fib/boot.asm /home/cc/vui/virts/c_native/fib/fib.c
	@mkdir -p /home/cc/vui/virts/c_native/fib/build
	@nasm -felf64 /home/cc/vui/virts/c_native/fib/boot.asm -o /home/cc/vui/virts/c_native/fib/build/boot.o
	@gcc -O3 -nostdlib -c -o /home/cc/vui/virts/c_native/fib/build/fib.o /home/cc/vui/virts/c_native/fib/fib.c
	@ld -T /home/cc/vui/virts/c_native/fib/rt.ld -o /home/cc/vui/virts/c_native/fib/build/fib.elf /home/cc/vui/virts/c_native/fib/build/boot.o /home/cc/vui/virts/c_native/fib/build/fib.o
	@objcopy -O binary /home/cc/vui/virts/c_native/fib/build/fib.elf /home/cc/vui/virts/c_native/fib/build/fib.bin