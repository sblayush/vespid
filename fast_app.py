from fastapi import FastAPI, Response, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from api.utilities.utilities import get_dir_path, create_dir, read_json
from api.actions.CAction import CAction
from api.actions.JSAction import JSAction
from api.initialize import initialize

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

app.mount(
    "/static",
    StaticFiles(directory="{}/static".format(_APP_PATH)),
    name="static",
)
actions_map = {}

@app.get("/ping")
def ping(response: Response):
    response.status_code = 200
    return "pong"


class CodeParam(BaseModel):
    vcode: str

class ArgParam(BaseModel):
    vargs: str


@app.post("/actions/{vname}/create")
def create(vname: str, code: CodeParam, response: Response):
	"""
	Create an action
	"""
	logging.info(
	"""Got request '/actions/{}/create' with params:
		vname- {}""".format(vname, vname))
	if not vname:
		resp = {"resp": "No vname data"}
		response.status_code = 400
		return resp
	vcode = code.vcode
	language = 'c'
	
	if vname in actions_map:
		resp = {"resp": "Action already exists"}
		response.status_code = 400
		return resp

	if language == 'c':
		act = CAction()
	else:
		act = JSAction()
	res = act.create(vname, vcode)

	actions_map[vname] = act

	resp = {"resp": res}
	return resp


@app.post("/actions/{vname}/invoke")
def invoke(vname, args: ArgParam, response: Response):
	"""
	Invoke an action
	"""
	logging.info(
	"""Got request '/actions/{}/invoke' with params:
		vname- {}""".format(vname, vname))
	if not vname:
		resp = {"resp": "No vname data"}
		response.status_code = 400
		return resp
	args = args.vargs
	
	if vname not in actions_map:
		resp = {"resp": "Action '{}' does not exist".format(vname)}
		response.status_code = 400
		return resp

	act = actions_map[vname]
	res = act.invoke(args)

	resp = {"resp": res}
	return resp


@app.get("/actions/{vname}/get")
def get(vname, response: Response):
	if not vname:
		resp = {"resp": "No vname data"}
		response.status_code = 400
		return resp
	
	if vname not in actions_map:
		resp = {"resp": "Action '{}' does not exist".format(vname)}
		response.status_code = 400
		return resp

	act = actions_map[vname]
	res = act.get()

	resp = {"resp": res}
	return resp

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
	with open("/home/cc/vui/templates/index.html", 'r') as f:
		html_content = f.read()
	return html_content

if __name__ == "__main__":
	uvicorn.run("fast_app:app", port=port, host=host, reload=rload)
