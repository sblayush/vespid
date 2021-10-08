# Notes

### Get the virtines project
```
git clone git@github.com:HExSA-Lab/vm-funcs.git
```
 
### install and build llvm (https://llvm.org/docs/GettingStarted.html#example-with-clang)
```
git clone https://github.com/llvm/llvm-project.git
cd llvm-project/
mkdir build
cd build/
```

### make Ninja
```
cmake -G Ninja ../llvm
```

### build everything (might not be strictly required to build all, but I am not sure of the dependencies)
```
cmake --build .
cd ../..
```

### install clang if not there
```which clang
sudo apt install clang

cd vm-funcs/
```

### build wasp
```
cd wasp/
make
sudo make install
#That will make and install wasp, a library that the pass utilizes.

cd ..
```

### build pass
```
cd pass/
sudo make
sudo make install

cd ..
```

### you can now use vcc to compile virtine programs like so
```
vcc pass/tests/add.c -o add
./add
```

### other dependencies that might be required
```
apt-get install nasm
sudo apt-get install cmake cmake-doc ninja-build
openssl
```

### open a port for tcp service
```
sudo ufw allow 8989/tcp
```
