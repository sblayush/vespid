from api.actions.ActionsManagerInterface import ActionsManagerInterface
from api.utilities.utilities import create_dir, get_dir_path
from api.common.error import *
from api.actions.CAction import CAction
from api.actions.JSAction import JSAction
import logging
import pickle

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
		else:
			act = JSAction()
		if act.create(vname, vcode) == RC_OK:
			self.actions[vname] = act
			self.save_action(vname)
			return "{} created successfully".format(vname)
		else:
			return "Unknown error creating actions"

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
		if vname not in self.actions:
			raise InvalidActionError(vname)
		return self.actions[vname].invoke(args)

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
