from app.core.config import env_config
from app.core.logger.elasticsearch_logger import es_logger
from app.elastic_search.config.index import Index
from app.elastic_search.config.template import Template
from elasticsearch import AsyncElasticsearch


class AsyncElasticsearchClient:

    def __init__(self):
        self.logger = es_logger
        self.client = AsyncElasticsearch(**env_config.ES_CONFIG)

    async def close(self):
        await self.client.close()

    async def search(self, body: dict, index: Index, params: dict = None):
        return await self.client.search(body=body, index=index.lower(), params=params)

    async def search_template(self, template: Template, index: Index):
        return await self.client.search_template(body=template.body, index=index.lower())

    # async def aaa(self):
    #     aa = ["ㄱ", "ㄴ", "ㄷ", "ㄹ", "ㅁ", "ㅂ", "ㅅ", "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]
