from app.elastic_search.engine.client import AsyncESClient
from app.model.dto.category_dto import Category
from app.model.enum.index import Index
from app.service.category_service import CategoryService


class CategoryServiceImpl(CategoryService):
    def __init__(self, es_client: AsyncESClient):
        self.es_client = es_client

    async def get_categories(self) -> list[Category]:
        body = {"query": {"match_all": {}}}

        params = {"size": 100}

        if self.es_client.client is None:
            await self.es_client.connect()

        result = await self.es_client.search(body, Index.PROVIDER, params)

        if result is None:
            return []

        return [Category(**hit["_source"]) for hit in result["hits"]["hits"]]
