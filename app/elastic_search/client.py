from elasticsearch import AsyncElasticsearch

from app.core.logger.elasticsearch_logger import es_logger
from app.model.enum.index import Index


class AsyncESClient:
    def __init__(self):
        self.client = AsyncElasticsearch(
            hosts="http://localhost:9200",
            basic_auth=("elastic", "42maru"),
        )
        self.logger = es_logger

    async def connect(self):
        self.client = AsyncElasticsearch(
            hosts="http://localhost:9200",
            timeout=60,
            max_retries=2,
            retry_on_timeout=True,
            sniff_on_start=False,
            maxsize=10,
        )

        ping_result = await self.client.ping()
        self.logger.connect(ping_result)

    async def close(self):
        if self.client:
            await self.client.close()
            self.client = None
            self.logger.close()

    async def search(self, body: dict, index: Index, params: dict):
        if self.client:
            return await self.client.search(body=body, index=index.lower(), params=params)

        return None
