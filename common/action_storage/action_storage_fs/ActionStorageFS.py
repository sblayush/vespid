from this import d
from common.action_storage.ActionStorageInterface import ActionStorageInterface
from common.utilities.utilities import create_dir, get_dir_path, does_dir_exist, remove_file
from common.error import *
import pickle
import json
import logging

_PWD = get_dir_path()
_ACTIONS_PATH = "{}/virts/actions".format(_PWD)


class ActionStorageFS(ActionStorageInterface):
	def __init__(self) -> None:
		self.initial_checks()
		self.actions_list = None
		self.load_actions_list()

	def initial_checks(self):
		create_dir(_ACTIONS_PATH)
		actions_list_path = "{}/actions_list.json".format(_ACTIONS_PATH)
		if not does_dir_exist(actions_list_path):
			with open(actions_list_path, 'w') as f:
				json.dump([], f)

	def load_action(self, vname):
		if vname not in self.actions_list:
			raise InvalidActionError(vname)
		try:
			with open("{}/action_{}.pkl".format(_ACTIONS_PATH, vname), "rb") as f:
				return pickle.load(f)
		except:
			logging.exception("No actions to load!")

	def load_actions_list(self):
		with open("{}/actions_list.json".format(_ACTIONS_PATH), 'r') as f:
			self.actions_list = json.load(f)
		return self.actions_list

	def save_actions_list(self):
		with open("{}/actions_list.json".format(_ACTIONS_PATH), 'w') as f:
			json.dump(self.actions_list, f)

	def save_action(self, vname, action):
		if vname not in self.actions_list:
			self.actions_list.append(vname)
		with open("{}/action_{}.pkl".format(_ACTIONS_PATH, vname), "wb") as f:
			pickle.dump(action, f)
		self.save_actions_list()

	def update_action(self):
		pass

	def delete_action(self, vname):
		if vname in self.actions_list:
			self.actions_list.remove(vname)
		remove_file("{}/action_{}.pkl".format(_ACTIONS_PATH, vname))
