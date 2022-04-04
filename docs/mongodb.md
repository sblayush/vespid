# Vespid mongodb setup

### setup mongodb
- Follow the steps in the [link](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/) to install and test mongodb
- open port 27017 (default)
  ```bash
	sudo ufw allow <port>/tcp
	```
- add the ip address of this server to appConfig.dat file in config path