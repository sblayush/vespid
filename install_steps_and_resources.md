# Notes


### Install dependencies
```
sudo apt install nasm
sudo apt-get install cmake cmake-doc ninja-build -y

wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key|sudo apt-key add -
# Fingerprint: 6084 F3CF 814B 57C1 CF12 EFD5 15CF 4D18 AF4F 7421

# LLVM
sudo apt-get install libllvm-12-ocaml-dev libllvm12 llvm-12 llvm-12-dev llvm-12-doc llvm-12-examples llvm-12-runtime -y

# Clang and co
sudo apt-get install clang-12 clang-tools-12 clang-12-doc libclang-common-12-dev libclang-12-dev libclang1-12 clang-format-12 clangd-12 -y
```

### Link llc and clang
```
sudo ln -s /usr/bin/clang-12 /usr/bin/clang
sudo ln -s /usr/bin/clang++-12 /usr/bin/clang++
sudo ln -s /usr/bin/llc-12 /usr/bin/llc
```

### Clone the virtines project
```
git clone git@github.com:HExSA-Lab/vm-funcs.git
```
 

### build wasp
```
cd wasp/
make
sudo make install
#That will make and install wasp, a library that the pass utilizes.
```

### build pass
```
cd pass/
sudo make
sudo make install
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
pip install flask fastapi
pip install pydantic
pip install uvicorn
pip install jinja2
```

### Open a port for tcp service
```
sudo ufw allow 8989/tcp
```

### Start server
```
cd vui
python3 fast_app.py
```

### Open in URL
```
http://192.5.86.153:8989/
```

### Additional notes
```
openssl
https://apt.llvm.org/
```




## OLD
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
pip install flask, fastapi
pip install pydantic
pip install uvicorn
pip install jinja2
```

### Open a port for tcp service
```
sudo ufw allow 8989/tcp
```

### Start server
```
cd vui
python3 fast_app.py
```

### Open in URL
```
http://192.5.86.153:8989/
```

### Additional notes
```
openssl
```
