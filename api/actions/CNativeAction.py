from api.actions.BaseAction import BaseAction
from api.utilities.utilities import create_dir, get_dir_path
from config.paths import wasp_shared_ob_path
from api.common.error import *
import subprocess
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

	def call_bin(self, args):
    class virt_buff(ctypes.Structure):
	    _fields_ = []
	    var_name = "a"
	    for a in args:
        _fields_.append((var_name, ctypes.c_int))
        var_name = chr(ord(var_name) + 1)
	    _fields_.append(("ret", ctypes.c_int))

		libname = wasp_shared_ob_path
		print(libname)
		c_lib = ctypes.CDLL(libname)
		virt_param = virt_buff(int(args[0]),3)

		var_name = "a"
    for a in args:
    	print("var_name", var_name, ", arg", a)
    	virt_param[var_name] = a
      var_name = chr(ord(var_name) + 1)

		n = ctypes.c_int(5)
		bin_path = "{}/{}/build/{}.bin".format(_CODE_PATH, self.action_name, self.action_name)


		#c_lib.wasp_native_test()
		with open(bin_path, mode='rb') as file: # b is important -> binary
			binary = file.read()
			file.seek(0, os.SEEK_END)
			c_lib.wasp_run_virtine(binary, file.tell(), 0x9000 + (file.tell() & ~0xFFF), ctypes.byref(virt_param), 16, None)
			return virt_param.ret

	def execute_code(self, vargs):
		try:
			start = time.time()
			args = [str(_) for _ in list(vargs.values())]
			res = self.call_bin(args)
			end = time.time()
			return {
				"result": res,
				"runTime": (end-start)*1000
			}
		except:
			raise  ActionInvokeError(self.action_name, err.decode())
