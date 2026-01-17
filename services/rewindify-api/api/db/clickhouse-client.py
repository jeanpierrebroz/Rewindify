'''
Sets up and fetches the clickhouse client.
'''
from clickhouse_connect.driver.client import Client
import os
from clickhouse_connect import get_client

CH_HOST = os.getenv("CH_HOST")
CH_PORT = int(os.getenv('CH_PORT', 8123))
CH_USER = os.getenv('CH_USER', '')
CH_PASS = os.getenv('CH_PASSWORD', default='')
CH_DB = os.getenv('CH_DB', '')

client: Client = get_client(
    host=CH_HOST,
    port=CH_PORT,
    username=CH_USER,
    password=CH_PASS,
    database=CH_DB
)
