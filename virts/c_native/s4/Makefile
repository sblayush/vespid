default:/home/cc/vui/virts/c_native/s4/boot.asm /home/cc/vui/virts/c_native/s4/s4.c
	@mkdir -p /home/cc/vui/virts/c_native/s4/build
	@nasm -felf64 /home/cc/vui/virts/c_native/s4/boot.asm -o /home/cc/vui/virts/c_native/s4/build/boot.o
	@gcc -O3 -nostdlib -c -o /home/cc/vui/virts/c_native/s4/build/s4.o /home/cc/vui/virts/c_native/s4/s4.c
	@ld -T /home/cc/vui/virts/c_native/s4/rt.ld -o /home/cc/vui/virts/c_native/s4/build/s4.elf /home/cc/vui/virts/c_native/s4/build/boot.o /home/cc/vui/virts/c_native/s4/build/s4.o
	@objcopy -O binary /home/cc/vui/virts/c_native/s4/build/s4.elf /home/cc/vui/virts/c_native/s4/build/s4.bin