from app.elastic_search.client import AsyncElasticsearchClient
from app.elastic_search.config.index import Index
from app.elastic_search.config.template import SearchNews
from app.router.dto.search import SearchRequest, SearchResponse
from app.service.search_service import SearchService


class SearchServiceImpl(SearchService):
    async def search(
        self,
        request: SearchRequest,
        es_client: AsyncElasticsearchClient,
    ) -> SearchResponse:
        result = await es_client.search_template(SearchNews.from_request(request), Index.NEWS)
        return SearchResponse.from_result(result)
