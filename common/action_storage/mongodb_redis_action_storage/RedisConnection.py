import redis
import logging


class RedisConnection:
	def __init__(self, host, port):
		self.conn = self.create_db_connection(host, port)

	def create_db_connection(self, host, port):
		try:
			conn = redis.Redis(host=host, port=port, db=0)
			return conn
		except Exception as e:
			logging.exception(str(e))
