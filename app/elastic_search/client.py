from app.core.config import env_config
from app.core.logger.elasticsearch_logger import es_logger
from app.elastic_search.config.index import Index
from app.elastic_search.config.template import Template
from elasticsearch import AsyncElasticsearch


class AsyncElasticsearchClient:

    def __init__(self):
        self.logger = es_logger
        self.pit_time = env_config.ES_PIT_TIME
        self.client = AsyncElasticsearch(**env_config.ES_CONFIG)

    async def close(self):
        await self.client.close()

    async def open_point_im_time(self, index: Index) -> int:
        result = await self.client.open_point_in_time(index=index.lower(), keep_alive=self.pit_time)
        return result["id"]

    async def search(self, body: dict, index: Index) -> dict:
        return await self.client.search(body=body, index=index.lower())

    async def search_template(self, template: Template, index: Index) -> dict:
        return await self.client.search_template(body=template.body, index=index.lower())
