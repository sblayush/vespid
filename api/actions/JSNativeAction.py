from api.actions.BaseAction import BaseAction
from api.utilities.utilities import create_dir, get_dir_path, does_dir_exist
from config.paths import wasp_js_shared_ob_path
from api.common.error import *
import subprocess
import logging
import time
import ctypes
import os

func_code_template = """
var b64 = {}(10);
hcall_return(b64);"""

_PWD = get_dir_path()
_TEMP_PATH = "{}/temp/js_native".format(_PWD)
_CODE_PATH = "{}/virts/js_native".format(_PWD)
_BIN_PATH = "{}/virts/js_native".format(_PWD)

VIRTINE_PROC_IDENTIFIER = "virtine"

class JSNativeAction(BaseAction):
	def __init__(self):
		super().__init__()
		self.runtime = 'jsnative'

	def update_parameters(self, vcode):
		inp_params = vcode.split('(')[1].split(')')[0]
		for param in inp_params.split(','):
			param = param.strip()
			typ, nam = param.split(' ')
			self.parameters[nam] = typ

	def preprocess_action(self, vname, vcode):
		self.update_parameters(vcode)

	def cli_arg_convert(self, arg, typ):
		if(typ == "int"):
			return "atoi(" + arg + ")"

	def gen_c_func_file(self, vname, vcode):
		create_dir("{}/{}/".format(_CODE_PATH, self.action_name))
		self.action_code = vcode
		func_code = None
		with open("{}/func.c".format(_TEMP_PATH), 'r') as f:
			func_code = f.read()
		func_code = func_code.replace("####vcode####", vcode)

		with open("{}/{}/{}.c".format(_CODE_PATH, self.action_name, self.action_name), 'w') as f:
			f.write(func_code)

	def gen_make_file(self, vname):
		with open("{}/Makefile".format(_TEMP_PATH), 'r') as f:
			make_code = f.read()
		make_code = make_code.replace("####vname####", vname)
		make_code = make_code.replace("####code_path####", "{}/{}".format(_CODE_PATH, vname))

		with open("{}/{}/Makefile".format(_CODE_PATH, self.action_name), 'w') as f:
			f.write(make_code)

	def gen_boot_file(self, vname):
		with open("{}/boot.asm".format(_TEMP_PATH), 'r') as f:
			boot_code = f.read()
		boot_code = boot_code.replace("####vname####", vname)
		with open("{}/{}/boot.asm".format(_CODE_PATH, self.action_name), 'w') as f:
			f.write(boot_code)

	def gen_link_file(self, vname):
		with open("{}/rt.ld".format(_TEMP_PATH), 'r') as f:
			link_code = f.read()
		with open("{}/{}/rt.ld".format(_CODE_PATH, self.action_name), 'w') as f:
			f.write(link_code)

	def insert_code(self, vname, vcode):
		self.action_code = vcode
		func_code = func_code_template.format(vname)
		create_dir("{}/{}/".format(_CODE_PATH, self.action_name))
		vcode += func_code
		with open("{}/{}/func_{}.js".format(_CODE_PATH, self.action_name, self.action_name), 'w') as f:
			f.write(vcode)

	def compile_code(self):
		pass

	def call_bin(self, args):
		libname = wasp_js_shared_ob_path
		c_lib = ctypes.CDLL(libname)
		c_lib.js_x.restype = ctypes.c_char_p

		with open("{}/{}/func_{}.js".format(_CODE_PATH, self.action_name, self.action_name), 'r') as file:
			js_code = file.read().encode("utf-8")
			start = time.time()
			ret = c_lib.js_x(js_code)
			end = time.time()
			logging.log(logging.CRITICAL, "exec_native: "+str((end-start)*1000))
			return ret, (end-start)*1000

	def execute_code(self, vargs):
		try:
			args = [str(_) for _ in list(vargs.values())]
			res, exectime = self.call_bin(args)
			return {
				"result": res,
				"runTime": exectime
			}
		except:
			raise  ActionInvokeError(self.action_name, err.decode())
