from api.actions.BaseAction import BaseAction
from api.utilities.utilities import create_dir, get_dir_path
from api.common.error import *
import subprocess

_PWD = get_dir_path()
_TEMP_PATH = "{}/temp/c_shared".format(_PWD)
_CODE_PATH = "{}/virts/shared_c".format(_PWD)
_BIN_PATH = "{}/virts/bin".format(_PWD)
_EXEC_PATH = "{}/virts/exec".format(_PWD)

class CSharedAction(BaseAction):
	def __init__(self):
		self.runtime = 'c'
	

	def insert_code(self, vcode):
		self.action_code = vcode
		func_code = None
		with open("{}/func.c".format(_TEMP_PATH), 'r') as f:
			func_code = f.read()
		func_code = func_code.replace("####vcode####", vcode)
		create_dir("{}/{}/".format(_CODE_PATH, self.action_name))
		create_dir("{}/{}/".format(_EXEC_PATH, self.action_name))
		with open("{}/{}/func_{}.c".format(_CODE_PATH, self.action_name, self.action_name), 'w') as f:
			f.write(func_code)

	def compile_code(self):
		# create_binary if not present
		subprocess.call(
			["vcc", 
			"{}/{}/func_{}.c".format(_CODE_PATH, self.action_name, self.action_name), 
			"-o", "{}/{}/{}".format(_EXEC_PATH, self.action_name, self.action_name)])

	def execute_code(self, vargs):
		# pass args and binary env to wasp vm
		args = [str(_) for _ in list(vargs.values())]
		p = subprocess.Popen(
			["{}/{}/{}".format(_EXEC_PATH, self.action_name, self.action_name)]+args, 
			stdout=subprocess.PIPE)
		out, err = p.communicate()
		if not err:
			return out.decode()
		else:
			raise  ActionInvokeError(self.action_name, err.decode())
	