# Notes

### Install dependencies
```
sudo apt-get install nasm
sudo apt-get install cmake cmake-doc ninja-build
```

### Clone the virtines project
```
git clone git@github.com:HExSA-Lab/vm-funcs.git
```
 
### install and build llvm (https://llvm.org/docs/GettingStarted.html) with clang
```
git clone https://github.com/llvm/llvm-project.git
cd llvm-project/
mkdir build
cd build/

cmake -DLLVM_ENABLE_PROJECTS=clang -G Ninja ../llvm

cmake --build .
sudo cmake --build . --target install
cd ../..
```

### check if clang is there
```
which clang
cd ../vm-funcs
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

### Tets bu using vcc to compile virtine programs
```
vcc pass/tests/add.c -o add
./add
```

### Clone vui
```
git clone git@github.com:sblayush/vui.git
```

### Install python dependencies
```
pip install flask
```

### Open a port for tcp service
```
sudo ufw allow 8989/tcp
```

### Start server
```
cd vui
python3 app.py
```

### Open in URL
```
http://192.5.86.153:8989/
```

### Additional notes
```
openssl
```
