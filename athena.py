import os
import json
import boto3
import logging
import pandas as pd
from io import StringIO
# Remove back to .
from research_core.aws.s3 import AwsS3
from research_core.aws.iam import getUser
from research_core.aws.common import *

import tempfile
from datetime import *
import time

DB_CONFIG_PATH = "db_config"
DB_CONFIG_FILE_AGE = 7
DB_CONFIG_BUCKET = "rtz-internal-metadata"

RESULTS_PATH = "research_core"
RESULTS_BUCKET = "aws-athena-query-results-018108293200-"
MAX_READ_TIMEOUT = 5


class AwsAthena():
    def __init__(self, access_key='', secret_key='', region_name='eu-central-1'):
        self.s3 = AwsS3(access_key, secret_key)

        ''' 
            Initialize the database and the results file location
        '''
        self.database = ''
        self.region_name = region_name
        self.result_bucket_full_path = ''
        self.db_config_path = DB_CONFIG_PATH
        self.db_config_bucket = DB_CONFIG_BUCKET

        ''' 
            Get the current username to be use at the S3 path
        '''
        self.username = getUser()
        if self.username:
            self.result_bucket_path = self.username
        else:
            self.result_bucket_path = RESULTS_PATH

    def __init__athena_client(self, region_name, access_key='', secret_key=''):
        if access_key == '' and secret_key == '':
            self.client = boto3.client('athena', region_name=region_name)
        else:
            self.client = boto3.client('athena',
                                       region_name=region_name,
                                       aws_access_key_id=access_key,
                                       aws_secret_access_key=secret_key)

    def __get_database_region(self, database):

        '''
            Download the DB config file, if it not exist yet or if it older then DB_CONFIG_FILE_AGE
        '''
        local_db_temp_dir = tempfile.gettempdir()
        local_db_conf_file = os.path.join(local_db_temp_dir, database)

        if not os.path.exists(local_db_conf_file) or \
                is_file_older_than_days(local_db_conf_file, DB_CONFIG_FILE_AGE):
            config_filename = "{}/{}".format(self.db_config_path, database)
            if self.s3.is_exist(self.db_config_bucket, config_filename):
                res = self.s3.download_file('{}/{}'.format(self.db_config_bucket, config_filename), local_db_temp_dir)
            else:
                self.database = database
                return False

        try:
            database_file = open((local_db_conf_file), 'r')
            self.database = database
            self.region_name = database_file.read().rstrip()
            return True

        except Exception as e:
            print(e)
            logging.error(e)
            raise Exception(e)

        return False

    def __send_query(self, query, database):

        '''
            Update the database and the results file location based on the DB config
            If the DB config is not avalible, use the default location 
        '''
        if self.__get_database_region(database):
            self.__init__athena_client(self.region_name)
            self.results_bucket_name = RESULTS_BUCKET + self.region_name
            self.result_bucket_full_path = 's3://{}/{}'.format(self.results_bucket_name, self.result_bucket_path)

        else:
            # print("db_configuration file is missing - using the default location")
            self.__init__athena_client(self.region_name)
            self.results_bucket_name = RESULTS_BUCKET + self.region_name
            self.result_bucket_full_path = 's3://{}/{}'.format(self.results_bucket_name, self.result_bucket_path)

        '''
            Execution the athena query
        '''
        execution = self.client.start_query_execution(
            QueryString=query,
            QueryExecutionContext={'Database': database},
            ResultConfiguration={'OutputLocation': self.result_bucket_full_path}
        )
        execution_id = execution['QueryExecutionId']
        state = 'RUNNING'

        '''
            Wait for the query tp complete
        '''
        while state in ['RUNNING', 'QUEUED']:
            response = self.client.get_query_execution(QueryExecutionId=execution_id)
            if 'QueryExecution' in response and 'Status' in response['QueryExecution'] and 'State' in \
                    response['QueryExecution']['Status']:
                state = response['QueryExecution']['Status']['State']
                if state == 'FAILED' or state == 'CANCELLED':
                    return False
                elif state == 'SUCCEEDED':
                    return execution_id
            time.sleep(1)

    def run_query(self, query, database, result_format='df'):
        """
        Run query on AWS Athena
        :param query: query to run on athena
        :param database: name of database
        :param result_format: choose type of data returned. df = DataFrame (default), json = JSON format
        :return: query result
        """

        read_timeout = 0

        try:
            execution_id = self.__send_query(query, database)
            if not execution_id:
                raise Exception('query execution has failed')

            txt_filename = "{}/{}.txt".format(self.result_bucket_full_path, execution_id)
            if self.s3.is_exist(self.results_bucket_name, txt_filename):
                res = self.s3.read_file(txt_filename, self.results_bucket_name)
                self.s3.delete_file(txt_filename, self.results_bucket_name)
                self.s3.delete_file(txt_filename + ".metadata", self.results_bucket_name)
                return res

            csv_filename = "{}/{}.csv".format(self.result_bucket_full_path, execution_id)

            # Wait for the file to be written
            while self.s3.is_exist(self.results_bucket_name, csv_filename) in [False]:
                time.sleep(1)
                if read_timeout < MAX_READ_TIMEOUT:
                    read_timeout += 1
                else:
                    raise Exception("results file can't be located")

            res = self.s3.read_file(csv_filename, self.results_bucket_name)
            res = StringIO(res).getvalue().replace('\x00', '')
            df = pd.read_csv(StringIO(res))
            self.s3.delete_file(csv_filename, self.results_bucket_name)
            self.s3.delete_file(csv_filename + ".metadata", self.results_bucket_name)

            response_batch_get_query_execution = self.client.batch_get_query_execution(
                QueryExecutionIds=[execution_id]
            )

            for query in list(response_batch_get_query_execution.values())[0]:
                # print(
                #     query['QueryExecutionId'],
                #     query['Status']['SubmissionDateTime'],
                #     query['ResultConfiguration']['OutputLocation'],
                #     'ExecuteTime {} ms'.format(query['Statistics']['TotalExecutionTimeInMillis']),
                #     'QueueTime {} ms'.format(query['Statistics']['QueryQueueTimeInMillis']),
                # )
                pass
            if result_format == 'json':
                return json.loads(df.to_json(orient='records'))

            return df
        except Exception as e:
            # print(e)
            logging.error(e)
            raise Exception(e)


if __name__ == '__main__':
    aws = AwsAthena()
    query = """
    SELECT * FROM "columbus"."leads" limit 10
    """
    df = aws.run_query(query=query, database="columbus")
    print(df)
