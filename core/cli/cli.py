from cProfile import run
from typing import Optional
import typer
import json
import requests
import logging
import os

import sys
sys.path.append("/home/cc/ayush/vespid/")

from common.error import *

localenv_path = "/home/cc/ayush/vespid/core/cli/localenv"
app = typer.Typer()
localenv = json.load(open(localenv_path, 'r'))
filetype_map = {
	'js': 'jsnative',
	'c': 'cnative'
}

@app.command()
def seturl(url: str = typer.Argument(...)):
	r = requests.get(url=url)
	if r.status_code == 200:
		localenv["VESPID_URL"] = url
		typer.echo(f"Connected to {url}")
		json.dump(localenv, open(localenv_path, 'w'))
	else:
		typer.echo(f"{url} not found")

@app.command()
def isconnected():
	if "VESPID_URL" in localenv:
		typer.echo(f"Connected to {localenv['VESPID_URL']}")
	else:
		typer.echo(f"not connected")


def process_filename(filename):
	filename, extension = filename.split('.')
	if extension in filetype_map:
		return filetype_map[extension]
	else:
		raise InvalidRuntimeError()

@app.command()
def create(vname: str = typer.Argument(...), filename: str = typer.Argument(...)):
	"""
	Create an action
	"""
	try:
		if "VESPID_URL" in localenv:
			url = localenv['VESPID_URL']
		else:
			raise Exception()
		vcode = open(filename, 'r').read()
		runtime = process_filename(filename)
		if runtime not in {'c', 'js', 'cnative', 'jsnative'}:
			raise InvalidActionError("Unknown runtime: {}".format(runtime))
		data = {
			'vcode': vcode,
			'runtime': runtime
		}
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		r = requests.post("{}/actions/{}/create".format(url, vname), data=json.dumps(data), headers=headers)
		if r.status_code == 200:
			typer.echo(r.json()['result'])
		elif r.status_code == 500:
			typer.echo(r.json()['msg'])

	except Exception as e:
		logging.error(e)

@app.command()
def invoke(vname: str = typer.Argument(...), args: str = typer.Argument(...)):
	"""
	Invoke an action
	"""
	try:
		if "VESPID_URL" in localenv:
			url = localenv['VESPID_URL']
		else:
			raise Exception()
		data = json.dumps({
			'vargs': eval(args)
		})
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		r = requests.post("{}/actions/{}/invoke".format(url, vname), data=data, headers=headers)
		if r.status_code == 200:
			typer.echo(r.json()['result'])
		elif r.status_code == 500:
			typer.echo(r.json()['msg'])

	except Exception as e:
		logging.error(e)

@app.command()
def get(vname: str = typer.Argument(...)):
	"""
	Get an action
	"""
	try:
		if "VESPID_URL" in localenv:
			url = localenv['VESPID_URL']
		else:
			raise Exception()
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		r = requests.post("{}/actions/{}/get".format(url, vname), headers=headers)
		if r.status_code == 200:
			typer.echo(r.json()['result'])
		elif r.status_code == 500:
			typer.echo(r.json()['msg'])

	except Exception as e:
		logging.error(e)

@app.command()
def list(playgroundid: str = typer.Argument(...)):
	"""
	List actions
	"""
	try:
		if "VESPID_URL" in localenv:
			url = localenv['VESPID_URL']
		else:
			raise Exception()
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		data = json.dumps({
			'playgroundId': playgroundid
		})
		r = requests.post("{}/actions/list".format(url), headers=headers, data=data)
		if r.status_code == 200:
			typer.echo(r.json())
		elif r.status_code == 500:
			typer.echo(r.json()['msg'])

	except Exception as e:
		logging.error(e)


if __name__ == "__main__":
    app()