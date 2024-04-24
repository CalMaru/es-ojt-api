from typing import Union

from elasticsearch import AsyncElasticsearch

from app.core.config import env_config
from app.core.logging import logger


class AsyncESClient:
    def __init__(self):
        self.client: Union[AsyncElasticsearch, None] = None

    async def connect(self):
        self.client = AsyncElasticsearch(
            hosts=env_config.ES_CONFIG,
            basic_auth=(env_config.ES_USERNAME, env_config.ES_PASSWORD),
        )

        ping_result = await self.client.ping()
        logger.info(f"Connected to Elasticsearch: {ping_result}")

    async def close(self):
        if self.client:
            await self.client.close()
            self.client = None
            logger.info("Closed Elasticsearch client")
