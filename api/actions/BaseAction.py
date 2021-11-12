from api.actions.ActionInterface import ActionInterface
from api.common.error import *
import subprocess


class BaseAction(ActionInterface):
	def __init__(self):
		super().__init__()

	def insert_code(self, vcode):
		pass

	def compile_code(self):
		pass

	def execute_code(self, args):
		pass
	
	def create(self, vname, vcode):
		self.action_name = vname
		self.insert_code(vname, vcode)
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
