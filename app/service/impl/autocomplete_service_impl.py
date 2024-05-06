from app.elastic_search.client import AsyncElasticsearchClient
from app.elastic_search.config.index import Index
from app.elastic_search.config.template import AutocompleteNewsKeyword, AutocompleteReporter
from app.router.dto.autocomplete import AutocompleteResponse
from app.service.autocomplete_service import AutocompleteService


class AutocompleteServiceImpl(AutocompleteService):
    async def get_reporters(
        self,
        query: str,
        es_client: AsyncElasticsearchClient,
    ) -> AutocompleteResponse:
        template = AutocompleteReporter.from_query(query)
        result = await es_client.search_template(template, Index.REPORTER)
        return AutocompleteResponse.from_hits(result["hits"]["hits"])

    async def get_news_keywords(
        self,
        query: str,
        es_client: AsyncElasticsearchClient,
    ):
        template = AutocompleteNewsKeyword.from_query(query)
        result = await es_client.search_template(template, Index.NEWS)
        return AutocompleteResponse.from_hits(result["hits"]["hits"])
