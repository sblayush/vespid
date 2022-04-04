from core.actions.BaseAction import BaseAction
from common.utilities.utilities import create_dir, get_dir_path, rand_str
from config.paths import js_exec_path
from common.error import *
import subprocess
import logging
import time
import os

_PWD = get_dir_path()
_CODE_PATH = "{}/virts/js".format(_PWD)
func_code_template = """
var ret = {}(####vargs####);
hcall_return(ret);"""


class JSAction(BaseAction):
	def __init__(self):
		super().__init__()
		self.language = 'js'
		self.vcode = None

	def insert_code(self, vname, vcode):
		self.action_code = vcode
		func_code = func_code_template.format(vname)
		create_dir("{}/{}/".format(_CODE_PATH, self.action_name))
		vcode += func_code
		with open("{}/{}/func_{}.js".format(_CODE_PATH, self.action_name, self.action_name), 'w') as f:
			f.write(vcode)
		self.vcode = vcode

	def compile_code(self):
		pass

	def execute_code(self, vargs):
		start = time.time()
		rands = rand_str()
		js_code = self.vcode.replace("####vargs####", str(vargs))
		js_code_path = "{}/{}/func_{}_{}.js".format(_CODE_PATH, self.action_name, self.action_name, rands)
		with open(js_code_path, 'w') as f:
			f.write(js_code)
		print(js_code_path, js_exec_path)
		p = subprocess.Popen(
			[js_exec_path, js_code_path], 
			stdout=subprocess.PIPE)
		out, err = p.communicate()
		end = time.time()
		logging.log(logging.CRITICAL, "exec_js: "+str((end-start)*1000))
		os.remove(js_code_path)
		if not err:
			return {
				"result": out.decode(),
				"runTime": (end-start)*1000
			}
		else:
			raise  ActionInvokeError(self.action_name, err.decode())
