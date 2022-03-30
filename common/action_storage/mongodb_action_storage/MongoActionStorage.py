from common.action_storage.ActionStorageInterface import ActionStorageInterface
from common.action_storage.mongodb_action_storage.MongoConnection import MongoConnection
from common.utilities.utilities import get_dir_path, create_dir, read_json
from common.error import *
import bson
import pickle
import logging

_ACTIONS_DB_NAME = "actions_db"
_ACTIONS_COLLECTION_NAME = "actions_list"
_ACTION_COLLECTION_DICT = {
	'action_name': "",
	'action_pkl': bson.Binary(pickle.dumps("action object")),
	'params': {},
	'meta': {}
}
_APP_PATH = get_dir_path()
app_config = read_json("{}/config/appConfig.dat".format(_APP_PATH))
_MONGO_URL = app_config['mongo_url']


class MongoActionStorage(ActionStorageInterface):
	def __init__(self) -> None:
		self.conn = None
		self.initial_checks()

	def initial_checks(self):
		self.conn = MongoConnection(_MONGO_URL).conn
		# create actions database if not present
		self.conn[_ACTIONS_DB_NAME]
		# create actions_list collection if not present
		self.conn[_ACTIONS_DB_NAME][_ACTIONS_COLLECTION_NAME]

	def load_action(self, vname):
		try:
			query = {
				"action_name": vname
			}
			act = self.conn[_ACTIONS_DB_NAME][_ACTIONS_COLLECTION_NAME].find_one(query)
			if len(act) == 0:
				raise InvalidActionError(vname)
			return pickle.loads(act['action_pkl'])
		except Exception as e:
			logging.exception(str(e))

	def get_actions_list(self):
		actions_list = []
		for doc in self.conn[_ACTIONS_DB_NAME][_ACTIONS_COLLECTION_NAME].find({},{ "action_name": 1}):
			actions_list.append(doc['action_name'])
		return actions_list

	def save_action(self, vname, action):
		self.conn[_ACTIONS_DB_NAME][_ACTIONS_COLLECTION_NAME].insert_one({
			'action_name': vname,
			'action_pkl': bson.Binary(pickle.dumps(action)),
			'params': action.parameters,
			'meta': {}
		})

	def update_action(self):
		pass

	def delete_action(self, vname):
		try:
			query = {
				"action_name": vname
			}
			self.conn[_ACTIONS_DB_NAME][_ACTIONS_COLLECTION_NAME].delete_one(query)
		except Exception as e:
			logging.exception(str(e))
