default:####code_path####/boot.asm ####code_path####/####vname####.c
	@mkdir -p ####code_path####/build
	@nasm -felf64 ####code_path####/boot.asm -o ####code_path####/build/boot.o
	@gcc -O3 -nostdlib -c -o ####code_path####/build/####vname####.o ####code_path####/####vname####.c
	@ld -T ####code_path####/rt.ld -o ####code_path####/build/####vname####.elf ####code_path####/build/boot.o ####code_path####/build/####vname####.o
	@objcopy -O binary ####code_path####/build/####vname####.elf ####code_path####/build/####vname####.bin