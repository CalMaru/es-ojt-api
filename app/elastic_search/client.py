from elasticsearch import AsyncElasticsearch

from app.core.config import env_config
from app.core.logging import logger
from app.model.enum.index import Index


class AsyncESClient:
    def __init__(self):
        self.client = AsyncElasticsearch(hosts="http://localhost:9200",
                                         basic_auth=("elastic", "42maru"),)

    async def connect(self):
        print(f"username: {env_config.ES_USERNAME}")
        self.client = AsyncElasticsearch(
            hosts="http://localhost:9200",
            timeout=60,
            max_retries=2,
            retry_on_timeout=True,
            sniff_on_start=False,
            maxsize=10,
        )

        ping_result = await self.client.ping()
        print(f"ping_result: {ping_result}")
        logger.info(f"Connected to Elasticsearch: {ping_result}")

    async def close(self):
        if self.client:
            await self.client.close()
            self.client = None
            logger.info("Closed Elasticsearch client")

    async def search(self, body: dict, index: Index, params: dict):
        if self.client:
            return await self.client.search(body=body, index=index.lower(), params=params)

        return None
