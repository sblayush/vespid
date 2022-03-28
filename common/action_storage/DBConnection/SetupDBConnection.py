import os
import sqlite3
import sys
from sqlite3 import Error
import pandas as pd

from DBConnection.SqlQuery import sql_table_exist_query, \
    sql_create_pipeline_table_query, sql_create_component_table_query, sql_create_artifacts_table_query
from DBConnection.SqlQuery import pipeline_table_name, component_table_name, artifacts_table_name


class DBConnection:
    def __init__(self, db_file_path, type='sqlite'):
        if type == 'sqlite':
            self.conn = self.create_db_connection_sqlite(db_file_path)
        elif type == 'sql':
            self.conn = self.create_db_connection_sql(db_file_path)
        self.prepare_tables()

    def create_db_connection_sql(self, db_file):
        import pyodbc
        try:
            conn = pyodbc.connect(db_file)
            print('Succesfully connected to database... ', db_file)
            return conn
        except Error as e:
            print(e)

    def create_db_connection_sqlite(self, db_file):
        if os.path.exists(db_file):
            print('Database already exists... ', db_file)
        else:
            print('Database does not exists. Creating new database at... ', db_file)
        try:
            conn = sqlite3.connect(db_file)
            print('Succesfully connected to database... ', db_file)
            return conn
        except Error as e:
            print(e)

    # TODO: Added additional function
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

    def create_table(self, create_table_sql):
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
            self.conn.commit()
        except Error as e:
            print(e)

    def table_exists(self, table_name):
        c = self.conn.cursor()
        c.execute(sql_table_exist_query, [table_name])

        if c.fetchone()[0] == 1:
            print('Table {} exists.'.format(table_name))
            return True
        else:
            print('{} table does not exists in database....'.format(table_name))
            return False

    def prepare_tables(self):
        if not self.table_exists(pipeline_table_name):
            self.create_table(sql_create_pipeline_table_query)
            print('Successfully Created pipeline_run table in database...')
        if not self.table_exists(component_table_name):
            self.create_table(sql_create_component_table_query)
            print('Successfully created component_run table in database....')
        if not self.table_exists(artifacts_table_name):
            self.create_table(sql_create_artifacts_table_query)
            print('Successfully created artifacts_store table in database....')

    def insert_record(self, sql_query, data):
        cur = self.conn.cursor()
        cur.execute(sql_query, data)
        self.conn.commit()

    # print n last rows from the table
    def select_all(self, table_name, nrows=0):
        sql_select_query = """SELECT * FROM {}""".format(table_name)
        print(pd.read_sql_query(sql_select_query, self.conn)[-nrows:])

    def update_table(self, sql_query, data):
        cur = self.conn.cursor()
        cur.execute(sql_query, data)
        self.conn.commit()
