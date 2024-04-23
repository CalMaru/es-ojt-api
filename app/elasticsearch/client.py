from typing import Union

from elasticsearch import Elasticsearch

from app.core import logger
from app.core.config import env_config


class ESClient:
    def __init__(self):
        self.client: Union[Elasticsearch, None] = None

    def connect(self):
        self.client = Elasticsearch(
            hosts=env_config.ES_CONFIG,
            basic_auth=(env_config.ES_USERNAME, env_config.ES_PASSWORD),
        )

        ping_result = self.client.ping()
        logger.info(f"Connected to Elasticsearch: {ping_result}")

    def close(self):
        if self.client:
            self.client.close()
            self.client = None
            logger.info("Closed Elasticsearch client")
