from typing import Union

from app.elastic_search.client import AsyncElasticsearchClient
from app.elastic_search.config.index import Index
from app.elastic_search.template.template import SearchNews
from app.model.dto.search_dto import SearchRequest, SearchResponse
from app.service.keyword_service import KeywordService
from app.service.search_service import SearchService


class SearchServiceImpl(SearchService):
    def __init__(self, keyword_service: KeywordService):
        self.keyword_service = keyword_service

    async def search(
        self,
        request: SearchRequest,
        es_client: AsyncElasticsearchClient,
    ) -> SearchResponse:
        alternated_query = None

        if request.pit_id is None:
            request.pit_id = await es_client.open_point_im_time(Index.NEWS)

        if await self.is_alternative_search(request, es_client):
            request.query = await self.get_alternative_query(request, es_client)
            alternated_query = request.query

        template = SearchNews.from_request(request)
        result = await es_client.search_template(template, Index.NEWS)
        return SearchResponse.from_result(result, alternated_query, request)

    async def is_alternative_search(
        self,
        request: SearchRequest,
        es_client: AsyncElasticsearchClient,
    ) -> bool:
        if request.search_alternative is False:
            return False
        if request.search_after is not None:
            return False
        if await self.keyword_service.is_terms_exist(request.query, es_client):
            return False
        return True

    async def get_alternative_query(
        self,
        request: SearchRequest,
        es_client: AsyncElasticsearchClient,
    ) -> Union[str, None]:
        alternatives = await self.keyword_service.autocomplete(
            query=request.query,
            index=Index.KEYWORD,
            key="item",
            es_client=es_client,
        )
        suggestions = alternatives.suggestions

        if len(suggestions) == 0:
            return None
        return suggestions[0]
