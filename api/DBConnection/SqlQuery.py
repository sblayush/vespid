from config.config import db_type

"""
This file contain SQL Queries used for create and updating database.
"""

# Sql Table names
pipeline_table_name = 'pipeline_run'
component_table_name = 'component_run'
artifacts_table_name = 'artifacts_store'

# SQL table exists query
if db_type == 'sqlite':
	sql_table_exist_query = ''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name=? '''
elif db_type == 'sql':
	sql_table_exist_query = '''SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = ?'''
else:
	sql_table_exist_query = None

# SQL create table commands
sql_create_pipeline_table_query = """ CREATE  TABLE  {} (
                                                 run_id  NVARCHAR(10) PRIMARY KEY,
                                                 pipeline_name NVARCHAR(100) NOT NULL,
                                                 root_path NVARCHAR(500) NOT NULL,
                                                 components NVARCHAR(500) NOT NULL,
                                                 num_components INT NOT NULL,
                                                 run_date date,
                                                 start_time NVARCHAR(20),
                                                 end_time NVARCHAR(20),
                                                 status VARCHAR(20));
                                                 """.format(pipeline_table_name)

sql_create_component_table_query = """ CREATE  TABLE {} (
                                                 run_id  NVARCHAR(10)  NOT NULL,
                                                 pipeline_name NVARCHAR(100) NOT NULL,
                                                 component_name NVARCHAR(50) NOT NULL,
                                                 artifacts NVARCHAR(500),
                                                 execution_order INT NOT NULL,
                                                 start_time NVARCHAR(20),
                                                 end_time NVARCHAR(20),
                                                 error NVARCHAR(500),
                                                 status VARCHAR(20),
                                                 PRIMARY KEY (run_id, pipeline_name, component_name)
                                                 );
                                                 """.format(component_table_name)

sql_create_artifacts_table_query = """ CREATE  TABLE {} (
												artifact_id INTEGER PRIMARY KEY AUTOINCREMENT,
												run_id NVARCHAR(10)  NOT NULL,
												pipeline_name NVARCHAR(100) NOT NULL,
												component_name NVARCHAR(50) NOT NULL,
												artifact NVARCHAR(50),
												artifact_path NVARCHAR(250),
												start_time NVARCHAR(20),
												end_time NVARCHAR(20),
												status VARCHAR(20),
												size INTEGER
												);
												 """.format(artifacts_table_name)

# SQL insert commands for tables
sql_insert_pipeline_table_query = """ INSERT INTO {} values(?,?,?,?,?,?,?,?,?)""".format(pipeline_table_name)
sql_insert_component_table_query = """ INSERT INTO {} values(?,?,?,?,?,?,?,?,?)""".format(component_table_name)
sql_insert_atrifacts_table_query = """ INSERT INTO {} values(?,?,?,?,?,?,?,?,?)""".format(artifacts_table_name)

# SQL update commands for tables
sql_update_end_pipeline_table_query = """UPDATE {} SET status=?,end_time=? WHERE run_id=?""".format(pipeline_table_name)

sql_update_start_component_table_query = """UPDATE {} SET status=?,start_time=?, artifacts=? WHERE run_id=? AND pipeline_name=? AND 
                                                                        component_name=?
                                                                         """.format(component_table_name)
sql_update_end_component_table_query = """UPDATE {} SET status=?,end_time=? WHERE run_id=? AND pipeline_name=? AND 
                                                                        component_name=?
                                                                         """.format(component_table_name)
