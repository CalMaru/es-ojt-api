from app.elastic_search.client import AsyncElasticsearchClient
from app.elastic_search.config.index import Index
from app.elastic_search.config.template import SearchNews
from app.model.dto.search_dto import SearchRequest, SearchResponse
from app.service.search_service import SearchService


class SearchServiceImpl(SearchService):
    async def search(
        self,
        request: SearchRequest,
        es_client: AsyncElasticsearchClient,
    ) -> SearchResponse:
        if request.pit_id is None:
            request.pit_id = await es_client.open_point_im_time(Index.NEWS)

        template = SearchNews.from_request(request)
        result = await es_client.search_template(template, Index.NEWS)

        # TODO result에서 count가 0인 경우 alternative 검색 수행

        return SearchResponse.from_result(result, request.source, request.highlight)
