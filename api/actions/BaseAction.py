from api.actions.ActionInterface import ActionInterface
from api.utilities.utilities import create_dir, get_dir_path
from api.common.error import *
import subprocess


_PWD = get_dir_path()
_TEMP_PATH = "{}/temp".format(_PWD)
_CODE_PATH = "{}/virts/c".format(_PWD)
_EXEC_PATH = "{}/virts/exec".format(_PWD)

class BaseAction(ActionInterface):
	def __init__(self):
		pass

	def insert_code(self, vcode):
		pass

	def compile_code(self):
		pass

	def execute_code(self, args):
		pass
	
	def create(self, vname, vcode):
		self.action_name = vname
		self.insert_code(vcode)
		self.compile_code()
		return RC_OK
	
	def get(self):
		return {
			"name": self.action_name,
			"code": self.action_code
		}
	
	def update(self):
		pass

	def delete(self):
		pass

	def invoke(self, args):
		return self.execute_code(args)
