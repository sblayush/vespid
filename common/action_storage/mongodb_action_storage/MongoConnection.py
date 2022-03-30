from pymongo import MongoClient
import logging


class MongoConnection:
	def __init__(self, url):
		self.conn = self.create_db_connection(url)

	def create_db_connection(self, url):
		try:
			conn = MongoClient(url)
			return conn
		except Exception as e:
			logging.exception(str(e))

	def execute_query(self, query, should_commit=False, should_return=False, *args):
		print("Executing query: " + query)
		cursor = self.conn.cursor()
		result = None
		try:
			cursor.execute(query, *args)
			if should_commit:
				self.conn.commit()
			if should_return:
				result = cursor.fetchall()
		finally:
			cursor.close()
		return result

	def insert_record(self, sql_query, data):
		cur = self.conn.cursor()
		cur.execute(sql_query, data)
		self.conn.commit()

	def update_table(self, sql_query, data):
		cur = self.conn.cursor()
		cur.execute(sql_query, data)
		self.conn.commit()
