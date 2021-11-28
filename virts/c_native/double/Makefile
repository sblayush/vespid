default:/home/cc/vui/virts/c_native/double/boot.asm /home/cc/vui/virts/c_native/double/double.c
	@mkdir -p /home/cc/vui/virts/c_native/double/build
	@nasm -felf64 /home/cc/vui/virts/c_native/double/boot.asm -o /home/cc/vui/virts/c_native/double/build/boot.o
	@gcc -O3 -nostdlib -c -o /home/cc/vui/virts/c_native/double/build/double.o /home/cc/vui/virts/c_native/double/double.c
	@ld -T /home/cc/vui/virts/c_native/double/rt.ld -o /home/cc/vui/virts/c_native/double/build/double.elf /home/cc/vui/virts/c_native/double/build/boot.o /home/cc/vui/virts/c_native/double/build/double.o
	@objcopy -O binary /home/cc/vui/virts/c_native/double/build/double.elf /home/cc/vui/virts/c_native/double/build/double.bin