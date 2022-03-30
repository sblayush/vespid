from fastapi import FastAPI, Response, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.exceptions import RequestValidationError

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))).replace('\\', '/'))

from common.utilities.utilities import get_dir_path, create_dir, read_json
from ayush.vespid.core.action_manager.ActionsManager import ActionsManager
from common.error import *

from datetime import datetime
import time
import uvicorn
import logging

_APP_PATH = get_dir_path()
create_dir("{}/logs".format(_APP_PATH))
date_time = datetime.now()
log_filename = "{}/logs/test7_{}.log".format(
	_APP_PATH, time.mktime(date_time.timetuple()))
format = logging.Formatter(
	fmt='%(asctime)s [%(levelname)s] %(message)s', datefmt='%H:%M:%S')

logging.basicConfig(
    filename=log_filename,
    filemode='a+',
    format='%(asctime)s [%(levelname)s]%(message)s',
    datefmt='%H:%M:%S',
    level=logging.CRITICAL)

app_config = read_json("{}/config/appConfig.dat".format(_APP_PATH))

port = app_config['port']
host = app_config['host']
rload = app_config['reload']
n_workers = app_config['n_workers']

app = FastAPI()
AM = ActionsManager()

app.mount(
    "/core/standalone/ui/static",
    StaticFiles(directory="{}/core/standalone/ui/static".format(_APP_PATH)),
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
		if runtime not in {'c', 'js', 'cnative', 'jsnative'}:
			raise InvalidActionError("Unknown runtime: {}".format(runtime))
		logging.info(
		"""And: vcode- {}, runtime- {}""".format(vcode, runtime))
		resp = AM.create_action(vname, vcode, runtime)
		return resp

	except Exception as e:
		logging.error(e)
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
		logging.info(
		"""And: args- {}""".format(args))
		resp = AM.invoke_action(vname, args)
		return resp
	except Exception as e:
		logging.exception(e)
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
		logging.error(e)
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
		logging.error(e)
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
		logging.error(e)
		resp = {"msg": str(e)}
		response.status_code = e.status
		return resp


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
	with open(_APP_PATH + "/core/standalone/ui/templates/index.html", 'r') as f:
		html_content = f.read()
	return html_content

if __name__ == "__main__":
	uvicorn.run("app:app", port=port, host=host, reload=rload, workers=n_workers)
