from api.actions.ActionsManagerInterface import ActionsManagerInterface
from api.utilities.utilities import create_dir, get_dir_path
from api.common.error import *
from api.actions.CAction import CAction
from api.actions.CNativeAction import CNativeAction
from api.actions.JSAction import JSAction
import logging
import pickle
import time

_PWD = get_dir_path()
_ACTIONS_PATH = "{}/virts/actions".format(_PWD)


class ActionsManager(ActionsManagerInterface):
	def __init__(self):
		super().__init__()
		self.load_actions()

	def load_actions(self):
		try:
			with open("{}/actions.pkl".format(_ACTIONS_PATH), "rb") as f:
				self.actions = pickle.load(f)
		except:
			logging.exception("No actions to load!")

	def save_action(self, vname):
		create_dir(_ACTIONS_PATH)
		with open("{}/actions.pkl".format(_ACTIONS_PATH), "wb") as f:
			pickle.dump(self.actions, f)

	def create_action(self, vname, vcode, runtime):
		if vname in self.actions:
			raise ActionAlreadyExists(vname)
		if runtime == 'c':
			act = CAction()
		elif runtime == 'cnative':
			act = CNativeAction()
		elif runtime == 'js':
			act = JSAction()
		else:
			act = JSAction()
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
		if len(args) != len(act.parameters):
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
		if vname in self.actions:
			del self.actions[vname]
			self.save_action(vname)
			return "Action '{}' deleted successfully!".format(vname)
		else:
			raise InvalidActionError(vname)
