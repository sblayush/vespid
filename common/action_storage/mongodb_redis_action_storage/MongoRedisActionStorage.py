from common.action_storage.ActionStorageInterface import ActionStorageInterface
from common.action_storage.mongodb_action_storage.MongoConnection import MongoConnection
from common.action_storage.mongodb_redis_action_storage.RedisConnection import RedisConnection
from common.utilities.utilities import get_dir_path, read_json
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
_MONGO_HOST = app_config['mongo_host']
_MONGO_PORT = app_config['mongo_port']
_REDIS_HOST = app_config['redis_host']
_REDIS_PORT = app_config['redis_port']


class MongoRedisActionStorage(ActionStorageInterface):
	def __init__(self) -> None:
		self.mongo_conn = None
		self.redis_conn = None
		self.initial_checks()

	def initial_checks(self):
		self.mongo_conn = MongoConnection(_MONGO_HOST, _MONGO_PORT).conn
		# create actions database if not present
		self.mongo_conn[_ACTIONS_DB_NAME]
		# create actions_list collection if not present
		self.mongo_conn[_ACTIONS_DB_NAME][_ACTIONS_COLLECTION_NAME]

		self.redis_conn = RedisConnection(_REDIS_HOST, _REDIS_PORT).conn

	def load_action(self, vname):
		try:
			return pickle.loads(self.redis_conn.get('action_'+vname))
		except:
			try:
				query = {
					"action_name": vname
				}
				act = self.mongo_conn[_ACTIONS_DB_NAME][_ACTIONS_COLLECTION_NAME].find_one(query)
				if len(act) == 0:
					raise InvalidActionError(vname)
				if not self.redis_conn.set("action_"+vname, act['action_pkl']):
					raise InvalidActionError("Error in setting vname in redis"+vname)
				return pickle.loads(act['action_pkl'])
			except Exception as e:
				print(str(e))
				logging.exception(str(e))

	def get_actions_list(self):
		actions_list = []
		for doc in self.mongo_conn[_ACTIONS_DB_NAME][_ACTIONS_COLLECTION_NAME].find({},{ "action_name": 1}):
			actions_list.append(doc['action_name'])
		return actions_list

	def save_action(self, vname, action):
		self.mongo_conn[_ACTIONS_DB_NAME][_ACTIONS_COLLECTION_NAME].insert_one({
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
			self.mongo_conn[_ACTIONS_DB_NAME][_ACTIONS_COLLECTION_NAME].delete_one(query)
		except Exception as e:
			logging.exception(str(e))
