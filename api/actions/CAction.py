from api.actions.BaseAction import BaseAction
from api.utilities.utilities import create_dir, get_dir_path
from api.common.error import *
import subprocess

_PWD = get_dir_path()
_TEMP_PATH = "{}/temp/c/".format(_PWD)
_CODE_PATH = "{}/virts/c".format(_PWD)
_EXEC_PATH = "{}/virts/exec".format(_PWD)

class CAction(BaseAction):
	def __init__(self):
		super().__init__()
		self.runtime = 'c'
	
	def update_parameters(self, vcode):
		inp_params = vcode.split('(')[1].split(')')[0]
		for param in inp_params.split(','):
			param = param.strip()
			typ, nam = param.split(' ')
			self.parameters[nam] = typ

	def update_name(self, vname, vcode):
		return vcode.replace("main", vcode)

	def preprocess_action(self, vname, vcode):
		self.update_parameters(vcode)

	def insert_code(self, vname, vcode):
		self.preprocess_action(vname, vcode)
		vcode = self.update_name(vname, vcode)
		self.action_code = vcode
		func_code = None
		with open("{}/func.c".format(_TEMP_PATH), 'r') as f:
			func_code = f.read()
		func_code = func_code.replace("####vcode####", vcode)
		func_code = func_code.replace("####vname####", self.action_name)
		create_dir("{}/{}/".format(_CODE_PATH, self.action_name))
		create_dir("{}/{}/".format(_EXEC_PATH, self.action_name))
		with open("{}/{}/func_{}.c".format(_CODE_PATH, self.action_name, self.action_name), 'w') as f:
			f.write(func_code)

	def compile_code(self):
		subprocess.call(
			["vcc", 
			"{}/{}/func_{}.c".format(_CODE_PATH, self.action_name, self.action_name), 
			"-o", "{}/{}/{}".format(_EXEC_PATH, self.action_name, self.action_name)])

	def execute_code(self, vargs):
		args = [str(_) for _ in list(vargs.values())]
		p = subprocess.Popen(
			["{}/{}/{}".format(_EXEC_PATH, self.action_name, self.action_name)]+args, 
			stdout=subprocess.PIPE)
		out, err = p.communicate()
		if not err:
			return out.decode()
		else:
			raise  ActionInvokeError(self.action_name, err.decode())
	