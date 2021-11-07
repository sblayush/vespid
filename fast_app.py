from fastapi import FastAPI, Response, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.exceptions import RequestValidationError

from api.utilities.utilities import get_dir_path, create_dir, read_json
from api.actions.ActionsManager import ActionsManager
from api.VUIApp.VUIApp import VUIApp
from api.common.error import *

from datetime import datetime
import json
import uvicorn
import logging

_APP_PATH = get_dir_path()
create_dir("{}/logs".format(_APP_PATH))
log_filename = "{}/logs/log_{}.log".format(
	_APP_PATH, datetime.now().strftime('%d_%m_%Y'))
format = logging.Formatter(
	fmt='%(asctime)s [%(levelname)s] %(message)s', datefmt='%H:%M:%S')

app_config = read_json("{}/config/appConfig.dat".format(_APP_PATH))

port = app_config['port']
host = app_config['host']
rload = app_config['reload']

app = FastAPI()
AM = ActionsManager()

app.mount(
    "/static",
    StaticFiles(directory="{}/static".format(_APP_PATH)),
    name="static",
)

@app.get("/ping")
def ping(response: Response):
    response.status_code = 200
    return "pong"


class CodeParam(BaseModel):
	vcode: str
	runtime: str

class PlaygroundParam(BaseModel):
	playgroundId: str

class ArgParam(BaseModel):
    vargs: dict

def log_message(request: Request, e):
    print('start error'.center(60, '*'))
    print(f'{request.method} {request.url}')
    print(f'error is {e}')
    print('end error'.center(60, '*'))

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    log_message(request, exc)

@app.post("/actions/{vname}/create")
def create(vname: str, code: CodeParam, response: Response, request: Request):
	"""
	Create an action
	"""
	try:
		logging.info(
		"""Got request '/actions/{}/create' with params: vname- {}""".format(vname, vname))
		if not vname or not code:
			raise MissingArgumentError(vname)
		vcode = code.vcode
		runtime = code.runtime
		res = AM.create_action(vname, vcode, runtime)
		resp = {"result": "action '{}' created".format(vname)}
		return resp
		
	except Exception as e:
		resp = {"msg": str(e)}
		response.status_code = e.status
		return resp


@app.post("/actions/{vname}/invoke")
def invoke(vname, args: ArgParam, response: Response):
	"""
	Invoke an action
	"""
	try:
		logging.info(
		"""Got request '/actions/{}/invoke' with params: vname- {}""".format(vname, vname))
		if not vname:
			raise MissingArgumentError(vname)
		args = args.vargs
		res = AM.invoke_action(vname, args)
		resp = {"result": res}
		return resp
	except Exception as e:
		resp = {"msg": str(e)}
		response.status_code = e.status
		return resp


@app.post("/actions/{vname}/get")
def get(vname, response: Response):
	"""
	Get action info
	"""
	try:
		logging.info(
		"""Got request '/actions/{}/get' with params: vname- {}""".format(vname, vname))
		res = AM.get_action(vname)
		resp = {"result": res}
		return resp
	except Exception as e:
		resp = {"msg": str(e)}
		response.status_code = e.status
		return resp


@app.post("/actions/list")
def list(params: PlaygroundParam, response: Response):
	"""
	Get list of actions
	"""
	try:
		logging.info(
		"""Got request '/actions/list' with params: userid- {}""".format(params.playgroundId))
		res = AM.get_actions_list()
		resp = {"actions": res}
		return resp
	except Exception as e:
		resp = {"msg": str(e)}
		response.status_code = e.status
		return resp


@app.post("/actions/{vname}/delete")
def delete(vname, response: Response):
	"""
	Delete action
	"""
	try:
		logging.info(
		"""Got request '/actions/{}/delete' with params: vname- {}""".format(vname, vname))
		res = AM.delete_action(vname)
		resp = {"result": res}
		return resp
	except Exception as e:
		resp = {"msg": str(e)}
		response.status_code = e.status
		return resp


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
	with open("/home/cc/vui/templates/index.html", 'r') as f:
		html_content = f.read()
	return html_content

if __name__ == "__main__":
	uvicorn.run("fast_app:app", port=port, host=host, reload=rload)
