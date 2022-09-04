import sys
import os
import logging
import rds_config
import pymysql
import json
import csv
#rds settings
rds_host, rds_port  = os.environ['rds_endpoint'].split(":")
name = os.environ['db_username']
password = os.environ['db_password']
db_name = "ChallengeDB"


logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(host=rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
except:
    logger.error(f"ERROR: Unexpected error: Could not connect to MySql instance., rds_host is {rds_host}, db_name is {db_name}")
    sys.exit()

logger.info("SUCCESS: Connection to RDS mysql instance succeeded")

def handler(event, context):

    # get method
    if event.get("httpMethod") == "GET":
        return {
            'statusCode': 200,
            'body': 'DB connected and GET - method invoked.'
        }

    # post method
    if event.get("httpMethod") == "POST": 
        return {
            'statusCode': 200,
            'body': 'DB connected and POST - method invoked.'
        }

    # delete method
    if event.get("httpMethod") == "DELETE":
        return {
            'statusCode': 200,
            'body': 'DB connected and DELETE - method invoked.'
        }

