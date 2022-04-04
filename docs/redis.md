# Vespid redis setup

### setup redis
- Follow the steps in the [link](https://redis.io/docs/getting-started/) to install and test mongodb
- And this [link](https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-18-04)
- Python redis [documentation](https://github.com/redis/redis-py)
- open port 6379 (default)
  ```bash
	sudo ufw allow <port>/tcp
	```
- add the ip address of this server to appConfig.dat file in config path
- Some steps and config:
  ```bash
  # update redis.conf to apply supervised as systemd
  sudo vim /etc/redis/redis.conf
  # supervised systemd

  sudo systemctl daemon-reload
  sudo systemctl restart redis.service
  sudo systemctl status redis

  # update config to allow incoming requests and set eviction policy as lru
  sudo vim /etc/redis/redis.conf
  # bind 0.0.0.0 ::1
  # maxmemory-policy allkeys-lru

  sudo systemctl restart redis.service
  sudo systemctl status redis
  ```