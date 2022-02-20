# Notes


### Build Wasp
- Follow the steps to buid wasp [here](https://github.com/virtines/wasp#build-instructions)
- Also, make sure to ```make js``` to get the jsinterp.bin

### Install python dependencies
```
pip install flask fastapi
pip install pydantic
pip install uvicorn
pip install jinja2
pip3 install locust
```

### Clone vespid
```
git clone git@github.com:virtines/vespid.git
```

### Update configuration
- copy the config/paths.ex.py file to config/paths.py file and update the paths as required.
- copy the config/appConfig.ex.dat file to config/appConfig.dat file and update the app configurations as required.


### Open a port for tcp service
```
sudo ufw allow <port>/tcp
```

### Start server
```
cd vespid
python3 fast_app.py
```

### Open in URL
```
http://<host_ip>:<port>/
```
