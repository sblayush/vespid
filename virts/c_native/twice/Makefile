default:/home/cc/vui/virts/c_native/twice/boot.asm /home/cc/vui/virts/c_native/twice/twice.c
	@mkdir -p /home/cc/vui/virts/c_native/twice/build
	@nasm -felf64 /home/cc/vui/virts/c_native/twice/boot.asm -o /home/cc/vui/virts/c_native/twice/build/boot.o
	@gcc -O3 -nostdlib -c -o /home/cc/vui/virts/c_native/twice/build/twice.o /home/cc/vui/virts/c_native/twice/twice.c
	@ld -T /home/cc/vui/virts/c_native/twice/rt.ld -o /home/cc/vui/virts/c_native/twice/build/twice.elf /home/cc/vui/virts/c_native/twice/build/boot.o /home/cc/vui/virts/c_native/twice/build/twice.o
	@objcopy -O binary /home/cc/vui/virts/c_native/twice/build/twice.elf /home/cc/vui/virts/c_native/twice/build/twice.bin