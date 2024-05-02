from app.elastic_search.client import AsyncElasticsearchClient
from app.model.dto.category_dto import Category
from app.model.enum.index import Index
from app.service.category_service import CategoryService


class CategoryServiceImpl(CategoryService):
    async def get_categories(self, es_client: AsyncElasticsearchClient) -> list[Category]:
        body = {"query": {"match_all": {}}}
        params = {"size": 100}
        result = await es_client.search(body, Index.CATEGORY, params)

        return [Category(**hit["_source"]) for hit in result["hits"]["hits"]]
