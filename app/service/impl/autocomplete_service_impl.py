from app.elastic_search.client import AsyncElasticsearchClient
from app.elastic_search.config.index import Index
from app.model.dto.autocomplete_dto import AutocompleteResponse
from app.service.autocomplete_service import AutocompleteService
from app.service.keyword_service import KeywordService


class AutocompleteServiceImpl(AutocompleteService):
    def __init__(self, keyword_service: KeywordService):
        self.keyword_service = keyword_service

    async def get_reporters(
        self,
        query: str,
        es_client: AsyncElasticsearchClient,
    ) -> AutocompleteResponse:
        return await self.keyword_service.autocomplete(
            query=query,
            index=Index.REPORTER,
            key="name",
            es_client=es_client,
        )

    async def get_news_keywords(
        self,
        query: str,
        es_client: AsyncElasticsearchClient,
    ) -> AutocompleteResponse:
        return await self.keyword_service.autocomplete(
            query=query,
            index=Index.KEYWORD,
            key="item",
            es_client=es_client,
        )
