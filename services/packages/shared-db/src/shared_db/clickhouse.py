"""Sets up and fetches the clickhouse client."""

from clickhouse_connect import get_async_client
from clickhouse_connect.driver.asyncclient import AsyncClient
from dotenv import dotenv_values

config = dotenv_values()

CH_HOST = config.get("CH_HOST", "localhost")
CH_PORT = int(config.get("CH_PORT") or 8123)
CH_USER = config.get("CLICKHOUSE_USER", "default")
CH_PASS = config.get("CLICKHOUSE_PASSWORD", "")
CH_DB = config.get("CLICKHOUSE_DB", "rewindify_dev_db")

client: AsyncClient = get_async_client(
    host=CH_HOST,
    port=CH_PORT,
    username=CH_USER,
    password=CH_PASS,
    database=CH_DB,
)
