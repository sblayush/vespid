from api.actions.BaseAction import BaseAction
from api.utilities.utilities import create_dir, get_dir_path, rand_str
from config.paths import js_exec_path
from api.common.error import *
import subprocess
import logging
import time
import os

_PWD = get_dir_path()
_TEMP_PATH = "{}/temp".format(_PWD)
_CODE_PATH = "{}/virts/js".format(_PWD)
func_code_template = """
var ret = {}(####vargs####);
hcall_return(ret);"""


class JSAction(BaseAction):
	def __init__(self):
		super().__init__()
		self.language = 'js'
	

	def insert_code(self, vname, vcode):
		self.action_code = vcode
		func_code = func_code_template.format(vname)
		create_dir("{}/{}/".format(_CODE_PATH, self.action_name))
		vcode += func_code
		with open("{}/{}/func_{}.js".format(_CODE_PATH, self.action_name, self.action_name), 'w') as f:
			f.write(vcode)

	def compile_code(self):
		pass

	def execute_code(self, vargs):
		start = time.time()
		args = [str(_) for _ in list(vargs.values())]
		rands = rand_str()
		with open("{}/{}/func_{}.js".format(_CODE_PATH, self.action_name, self.action_name), 'r') as f:
			js_code = f.read().replace("####vargs####", str(vargs))
		with open("{}/{}/func_{}_{}.js".format(_CODE_PATH, self.action_name, self.action_name, rands), 'w') as f:
			f.write(js_code)
		p = subprocess.Popen(
			[js_exec_path, "{}/{}/func_{}_{}.js".format(_CODE_PATH, self.action_name, self.action_name, rands)], 
			stdout=subprocess.PIPE)
		out, err = p.communicate()
		end = time.time()
		logging.log(logging.CRITICAL, "exec_js: "+str((end-start)*1000))
		os.remove("{}/{}/func_{}_{}.js".format(_CODE_PATH, self.action_name, self.action_name, rands))
		if not err:
			return {
				"result": out.decode(),
				"runTime": (end-start)*1000
			}
		else:
			raise  ActionInvokeError(self.action_name, err.decode())
