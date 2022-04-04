from abc import ABC, abstractmethod

class ActionStorageInterface(ABC):
	def __init__(self) -> None:
		pass

	@abstractmethod
	def load_action(self, vname):
		pass

	@abstractmethod
	def get_actions_list(self):
		pass

	@abstractmethod
	def save_action(self, vname, action):
		pass

	@abstractmethod
	def update_action(self, vname, vcode):
		pass

	@abstractmethod
	def delete_action(self, vname):
		pass

