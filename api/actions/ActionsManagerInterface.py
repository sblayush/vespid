from abc import ABC, abstractmethod


class ActionsManagerInterface(ABC):
	def __init__(self):
		self.actions = {}

	@abstractmethod
	def load_actions(self):
		pass

	@abstractmethod
	def save_action(self, vname):
		pass

	@abstractmethod
	def create_action(self, vname, vcode):
		pass

	@abstractmethod
	def get_action(self, vname):
		pass

	@abstractmethod
	def invoke_action(self, vname, args):
		pass

	@abstractmethod
	def get_actions_list(self):
		pass

	@abstractmethod
	def update_action(self, vname, vcode):
		pass

	@abstractmethod
	def delete_action(self, vname):
		pass
