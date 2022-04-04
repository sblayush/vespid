from pymongo import MongoClient
import logging


class MongoConnection:
	def __init__(self, host, port):
		self.conn = self.create_db_connection(host, port)

	def create_db_connection(self, host, port):
		try:
			conn = MongoClient("mongodb://{}:{}/".format(host, port))
			return conn
		except Exception as e:
			logging.exception(str(e))
