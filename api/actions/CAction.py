from api.actions.BaseAction import BaseAction
from api.utilities.utilities import create_dir, get_dir_path
from api.common.error import *
import subprocess

_PWD = get_dir_path()
_TEMP_PATH = "{}/temp/c/".format(_PWD)
_CODE_PATH = "{}/virts/c".format(_PWD)
_EXEC_PATH = "{}/virts/exec".format(_PWD)

VIRTINE_PROC_IDENTIFIER = "virtine"

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

	# def update_name(self, vname, vcode):
	# 	print("vcode = " + vcode)
	# 	return vcode.replace("main", vcode)

	def preprocess_action(self, vname, vcode):
		self.update_parameters(vcode)

	def cli_arg_convert(self, arg, typ):
		if(typ == "int"):
			return "atoi(" + arg + ")";

	def insert_code(self, vname, vcode):
		self.preprocess_action(vname, vcode)
		# vcode = self.update_name(vname, vcode)

		plistdef = "\t";
		plistargs = "";

		argc = 1;
		for key in self.parameters:
			plistdef += self.parameters[key] + " " + key + " = " + self.cli_arg_convert("argv[" + str(argc) + "]", self.parameters[key]) + ";\n\t"
			plistargs += key + ", ";
			argc += 1;

		# remove the last semicolon
		plistargs = plistargs[:-2]

		self.action_code = vcode
		func_code = None
		with open("{}/func.c".format(_TEMP_PATH), 'r') as f:
			func_code = f.read()
		func_code = func_code.replace("####vcode####", vcode)
		func_code = func_code.replace("####vname####", self.action_name)
		func_code = func_code.replace("####plistdef####", plistdef)
		func_code = func_code.replace("####plistargs####", plistargs)

		create_dir("{}/{}/".format(_CODE_PATH, self.action_name))
		create_dir("{}/{}/".format(_EXEC_PATH, self.action_name))
		with open("{}/{}/func_{}.c".format(_CODE_PATH, self.action_name, self.action_name), 'w') as f:
			f.write(func_code)

	def compile_code(self):
		subprocess.call(
			["vcc",
			"{}/{}/func_{}.c".format(_CODE_PATH, self.action_name, self.action_name),
			"-o", "{}/{}/{}_{}".format(_EXEC_PATH, self.action_name, VIRTINE_PROC_IDENTIFIER, self.action_name)])

	def execute_code(self, vargs):
		args = [str(_) for _ in list(vargs.values())]
		p = subprocess.Popen(
			["{}/{}/{}_{}".format(_EXEC_PATH, self.action_name, VIRTINE_PROC_IDENTIFIER, self.action_name)]+args,
			stdout=subprocess.PIPE)
		out, err = p.communicate()
		if not err:
			return out.decode()
		else:
			raise  ActionInvokeError(self.action_name, err.decode())
