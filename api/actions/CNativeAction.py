from api.actions.BaseAction import BaseAction
from api.utilities.utilities import create_dir, get_dir_path, does_dir_exist
from config.paths import wasp_shared_ob_path
from api.common.error import *
import subprocess
import logging
import time
import ctypes
import os


_PWD = get_dir_path()
_TEMP_PATH = "{}/temp/c_native".format(_PWD)
_CODE_PATH = "{}/virts/c_native".format(_PWD)
_BIN_PATH = "{}/virts/c_native".format(_PWD)

VIRTINE_PROC_IDENTIFIER = "virtine"

class CNativeAction(BaseAction):
	def __init__(self):
		super().__init__()
		self.runtime = 'cnative'

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
		self.preprocess_action(vname, vcode)
		self.gen_c_func_file(vname, vcode)
		self.gen_boot_file(vname)
		self.gen_link_file(vname)
		self.gen_make_file(vname)

	def compile_code(self):
		create_dir("{}/{}/".format(_BIN_PATH, self.action_name))
		subprocess.call(["make", "-C", "{}/{}".format(_CODE_PATH, self.action_name)])
		
		bin_path = "{}/{}/build/{}.bin".format(_CODE_PATH, self.action_name, self.action_name)
		if not does_dir_exist(bin_path):
			raise ActionCompileError(self.action_name)
		return RC_OK

	def call_bin(self, args):
		class virt_buff(ctypes.Structure):
			# _fields_ = [("argc", ctypes.c_int)]
			_fields_ = []
			var_name = "a"
			for a in args:
				_fields_.append((var_name, ctypes.c_int))
				var_name = chr(ord(var_name) + 1)

			_fields_.append(("ret", ctypes.c_int))

		libname = wasp_shared_ob_path
		# print(self.action_name, self.parameters)
		c_lib = ctypes.CDLL(libname)

		eval_str = "virt_buff("
		# eval_str += str(len(args)) + ","
		for a in args:
			eval_str = eval_str + str(a) + ","

		eval_str += "0)"
		# print("eval_str", eval_str)
		virt_param = eval(eval_str)
		# print("virt_param.a", virt_param.a)

		bin_path = "{}/{}/build/{}.bin".format(_CODE_PATH, self.action_name, self.action_name)

		with open(bin_path, mode='rb') as file: # b is important -> binary
			binary = file.read()
			file.seek(0, os.SEEK_END)
			file_sz = file.tell()
			# hackey way to generate a unique cache
			key = 0x9000 + (abs(hash(self.action_name+self.action_code)) % 100)*4096
			# print("key=", key)
			start = time.time()
			c_lib.wasp_run_virtine(binary, file_sz, key + (file_sz & ~0xFFF), ctypes.byref(virt_param), (len(self.parameters)+1)*4, None)
			end = time.time()
			logging.log(logging.CRITICAL, "exec_native: "+str((end-start)*1000))
			return virt_param.ret, (end-start)*1000

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
