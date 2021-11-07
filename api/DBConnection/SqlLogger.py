import logging
from datetime import datetime

from common.error import *

from utilities.utilities import get_str_from_list
from DBConnection.SqlQuery import pipeline_table_name, component_table_name, sql_update_start_component_table_query, \
    sql_update_end_component_table_query, sql_update_end_pipeline_table_query, sql_insert_pipeline_table_query, \
    sql_insert_component_table_query


class SqlLogger:
    def __init__(self, db_conn, pipeline_name, root_path, component_names):
        self.db_conn = db_conn
        self.run_id = None
        self.pipeline_name = pipeline_name
        self.root_path = root_path
        if len(component_names) != len(set(component_names)):
            print('********************************************************')
            print('Given Pipeline contain duplicate components....therefore existing...')
            exit()
        self.component_names = component_names

    def set_run_id(self, run_id):
        self.run_id = run_id

    def pipeline_start(self):
        if not self.run_id:
            raise RunIDNotInitiatedException
        # Logging into pipeline table for an execution
        self.db_conn.update_table(sql_query=sql_insert_pipeline_table_query,
                                  data=[self.run_id, self.pipeline_name, self.root_path,
                                        get_str_from_list(
                                            [component for component in self.component_names]),
                                        len(self.component_names), datetime.today().strftime('%Y-%m-%d'),
                                        datetime.today().strftime('%H:%M:%S'), '', 'running'])

        # Logging different components details into component table
        for i, component_name in enumerate(self.component_names):
            artifacts = ''
            self.db_conn.update_table(sql_query=sql_insert_component_table_query,
                                      data=[self.run_id, self.pipeline_name, component_name,
                                            artifacts, i + 1, '', '', '', 'queue'])

    def pipeline_success(self):
        if not self.run_id:
            raise RunIDNotInitiatedException
        end_time = datetime.today().strftime('%H:%M:%S')
        self.db_conn.update_table(sql_query=sql_update_end_pipeline_table_query,
                                  data=['success', end_time, self.run_id])

    def pipeline_fail(self, failed_components):
        if not self.run_id:
            raise RunIDNotInitiatedException
        for i, component_name in enumerate(failed_components):
            if i == 0:
                self.component_fail(component_name)
            else:
                self.component_aborted(component_name)
        end_time = datetime.today().strftime('%H:%M:%S')
        self.db_conn.update_table(sql_query=sql_update_end_pipeline_table_query, data=['failed', end_time, self.run_id])

    def component_start(self, component_name, exp_outputs):
        if not self.run_id:
            raise RunIDNotInitiatedException
        artifacts = get_str_from_list(exp_outputs)
        start_time = datetime.today().strftime('%H:%M:%S')
        self.db_conn.update_table(sql_query=sql_update_start_component_table_query,
                                  data=['running', start_time, artifacts, self.run_id, self.pipeline_name,
                                        component_name])

    def component_success(self, component_name):
        if not self.run_id:
            raise RunIDNotInitiatedException
        end_time = datetime.today().strftime('%H:%M:%S')
        self.db_conn.update_table(sql_query=sql_update_end_component_table_query,
                                  data=['success', end_time, self.run_id, self.pipeline_name, component_name])

    def component_fail(self, component_name):
        if not self.run_id:
            raise RunIDNotInitiatedException
        end_time = datetime.today().strftime('%H:%M:%S')
        self.db_conn.update_table(sql_query=sql_update_end_component_table_query,
                                  data=['failed', end_time, self.run_id, self.pipeline_name, component_name])

    def component_aborted(self, component_name):
        if not self.run_id:
            raise RunIDNotInitiatedException
        end_time = datetime.today().strftime('%H:%M:%S')
        self.db_conn.update_table(sql_query=sql_update_end_component_table_query,
                                  data=['aborted', end_time, self.run_id, self.pipeline_name, component_name])
