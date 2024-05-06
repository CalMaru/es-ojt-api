from app.elastic_search.client import AsyncElasticsearchClient
from app.elastic_search.config.index import Index
from app.elastic_search.config.template import SearchNews
from app.router.dto.search import SearchElasticsearchRequest, SearchQueryRequest, SearchResponse
from app.service.search_service import SearchService


class SearchServiceImpl(SearchService):
    async def search(
        self,
        request: SearchQueryRequest,
        es_request: SearchElasticsearchRequest,
        es_client: AsyncElasticsearchClient,
    ) -> SearchResponse:
        if es_request.pit_id is None:
            es_request.pit_id = await es_client.open_point_im_time(Index.NEWS)

        template = SearchNews.from_requests(request, es_request)
        result = await es_client.search_template(template, Index.NEWS)
        return SearchResponse.from_result(result)
