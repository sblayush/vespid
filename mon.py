import signal
import sys
import _thread

# import time

from api.utilities.utilities import get_dir_path, create_dir, read_json
from fastapi import FastAPI, Response, Request
import uvicorn

# import virt_runtime.VirtMonitor
from monitor.monDaemon import VirtMonitor

_MON_PATH = get_dir_path()
mon_config = read_json("{}/config/monConfig.json".format(_MON_PATH))

PORT = mon_config['port']
HOST = mon_config['host']
ACTIVATE_LOGGER = mon_config["logger"]["active"]
LOG_PATH = mon_config["logger"]["path"]
MONITOR_POLLER_INTERVAL = mon_config["logger"]["interval"]

RLOAD = True

app = FastAPI()
vm = VirtMonitor(ACTIVATE_LOGGER, MONITOR_POLLER_INTERVAL, LOG_PATH);

@app.get("/")
async def root():
  return { "message": "This is virtine monitor." }

@app.get("/numinstances")
async def num_inst():
  return vm.num_instances()

@app.get("/stat")
async def stat_pid():
  return vm.all_virt_stat()

@app.get("/stat/{pid}")
async def stat_pid(pid):
  if not pid:
    raise MissingArgumentError(pid)

  return vm.stat_pid(pid)

@app.get("/ping")
async def get_pong():
  return vm.get_pong()

def start_http_server(name):
  uvicorn.run("mon:app", port = PORT, host = HOST, reload = RLOAD)

def start_daemon(name):
  vm.start_monitor()

if __name__ == "__main__":
  _thread.start_new_thread(start_daemon, ("vui-mon-daemon",) )
  start_http_server("vui-mon-http-server");
