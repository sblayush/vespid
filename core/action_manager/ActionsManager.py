from core.action_manager.ActionsManagerInterface import ActionsManagerInterface
from common.error import *
from common.action_storage.action_storage_fs.ActionStorageFS import ActionStorageFS
from core.action_manager.actions.CAction import CAction
from core.action_manager.actions.CNativeAction import CNativeAction
from core.action_manager.actions.JSAction import JSAction
from core.action_manager.actions.JSNativeAction import JSNativeAction
import logging
import time

action_class_map = {
	'c': CAction(),
	'cnative': CNativeAction(),
	'js': JSAction(),
	'jsnative': JSNativeAction()
}


class ActionsManager(ActionsManagerInterface):
	def __init__(self):
		super().__init__()
		self.action_storage = ActionStorageFS()
		self.load_actions()

	def load_actions(self):
		for vname in self.action_storage.load_actions_list():
			self.actions[vname] = self.action_storage.load_action(vname)
	
	def save_action(self, vname):
		self.action_storage.save_action(vname, self.actions[vname])

	def create_action(self, vname, vcode, runtime):
		if vname in self.actions:
			raise ActionAlreadyExists(vname)
		if runtime not in action_class_map:
			raise ActionCompileError("Undefined runtime")
		act = action_class_map[runtime]
		try:
			if act.create(vname, vcode) == RC_OK:
				self.actions[vname] = act
				self.save_action(vname)
				res = {
					"deployTime": 0,
					"runTime": 0,
					"result": "action '{}' created successfully".format(vname)
				}
				return res
			else:
				raise ActionCompileError("Unknown error creating actions")
		except Exception as e:
			logging.exception("Unknown error creating actions")
			raise ActionCompileError("Unknown error creating actions")

	def get_action(self, vname):
		if vname in self.actions:
			val = self.actions[vname]
			return {
				"vname": val.action_name,
				"vcode": val.action_code,
				"runtime": val.runtime
			}
		else:
			raise InvalidActionError(vname)

	def invoke_action(self, vname, args):
		start = time.time()
		if vname not in self.actions:
			raise InvalidActionError(vname)
		act = self.actions[vname]
		if act.runtime in {'c', 'cnative'} and len(args) != len(act.parameters):
			raise InvalidSignatureError(vname)
		res = self.actions[vname].invoke(args)
		end = time.time()
		res["deployTime"] = (end-start)*1000 - res["runTime"]
		return res

	def get_actions_list(self):
		al = []
		for action_name in self.actions:
			al.append(self.get_action(action_name))
		return al

	def update_action(self, vname, vcode):
		pass

	def delete_action(self, vname):
		self.action_storage.delete_action(vname)
		del self.actions[vname]
	