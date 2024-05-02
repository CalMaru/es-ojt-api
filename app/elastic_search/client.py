from elasticsearch import AsyncElasticsearch

from app.core.config import env_config
from app.core.logger.elasticsearch_logger import es_logger
from app.model.enum.index import Index


class AsyncElasticsearchClient:

    def __init__(self):
        self.logger = es_logger
        self.client = AsyncElasticsearch(**env_config.ES_CONFIG)

    async def close(self):
        await self.client.close()

    async def search(self, body: dict, index: Index, params: dict):
        return await self.client.search(body=body, index=index.lower(), params=params)
