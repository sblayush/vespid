from api.actions.ActionsManagerInterface import ActionsManagerInterface
from api.common.error import *
from api.actions.CAction import CAction
from api.actions.JSAction import JSAction


class ActionsManager(ActionsManagerInterface):
	def __init__(self):
		self.actions = {}
		self.load_actions()

	def load_actions(self):
		pass

	def save_action(self, vname):
		pass

	def create_action(self, vname, vcode, runtime):
		if vname in self.actions:
			raise ActionAlreadyExists(vname)
		if runtime == 'c':
			act = CAction()
		else:
			act = JSAction()
		if act.create(vname, vcode) == RC_OK:
			self.actions[vname] = act
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
			return "Action '{}' deleted successfully!"
		else:
			raise InvalidActionError(vname)
