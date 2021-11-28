default:/home/cc/vui/virts/c_native/add/boot.asm /home/cc/vui/virts/c_native/add/add.c
	@mkdir -p /home/cc/vui/virts/c_native/add/build
	@nasm -felf64 /home/cc/vui/virts/c_native/add/boot.asm -o /home/cc/vui/virts/c_native/add/build/boot.o
	@gcc -O3 -nostdlib -c -o /home/cc/vui/virts/c_native/add/build/add.o /home/cc/vui/virts/c_native/add/add.c
	@ld -T /home/cc/vui/virts/c_native/add/rt.ld -o /home/cc/vui/virts/c_native/add/build/add.elf /home/cc/vui/virts/c_native/add/build/boot.o /home/cc/vui/virts/c_native/add/build/add.o
	@objcopy -O binary /home/cc/vui/virts/c_native/add/build/add.elf /home/cc/vui/virts/c_native/add/build/add.bin