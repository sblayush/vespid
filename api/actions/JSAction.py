from api.actions.BaseAction import BaseAction
from api.utilities.utilities import create_dir, get_dir_path
from config.paths import js_exec_path
from api.common.error import *
import subprocess
import logging
import time

_PWD = get_dir_path()
_TEMP_PATH = "{}/temp".format(_PWD)
_CODE_PATH = "{}/virts/js".format(_PWD)
func_code_template = """
var b64 = {}();
hcall_return(b64);"""


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
		p = subprocess.Popen(
			[js_exec_path, "{}/{}/func_{}.js".format(_CODE_PATH, self.action_name, self.action_name)], 
			stdout=subprocess.PIPE)
		out, err = p.communicate()
		end = time.time()
		logging.log(logging.CRITICAL, "exec_c: "+str((end-start)*1000))
		if not err:
			return {
				"result": out.decode(),
				"runTime": (end-start)*1000
			}
		else:
			raise  ActionInvokeError(self.action_name, err.decode())
