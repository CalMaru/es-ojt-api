from app.elastic_search.client import AsyncElasticsearchClient
from app.service.search_service import SearchService


class SearchServiceImpl(SearchService):
    async def search(self, es_client: AsyncElasticsearchClient):
        return None
