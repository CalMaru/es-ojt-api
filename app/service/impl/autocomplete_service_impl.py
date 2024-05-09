import hgtk.checker
from gksdudaovld import KoEngMapper

from app.elastic_search.client import AsyncElasticsearchClient
from app.elastic_search.config.index import Index
from app.elastic_search.config.template import AutocompleteKeyword, AutocompleteReporter
from app.model.dto.autocomplete_dto import AutocompleteResponse
from app.service.autocomplete_service import AutocompleteService


class AutocompleteServiceImpl(AutocompleteService):
    async def get_reporters(
        self,
        query: str,
        es_client: AsyncElasticsearchClient,
    ) -> AutocompleteResponse:
        template = AutocompleteReporter.from_query(query)
        result = await es_client.search_template(template, Index.REPORTER)
        return AutocompleteResponse.from_hits(result["hits"]["hits"], "name")

    async def get_news_keywords(
        self,
        query: str,
        es_client: AsyncElasticsearchClient,
    ):
        if hgtk.checker.is_hangul(query) is False:
            query = KoEngMapper.conv_en2ko(query)

        template = AutocompleteKeyword.from_query(query)
        result = await es_client.search_template(template, Index.KEYWORD)

        count = result["hits"]["total"]["value"]
        if count > 0:
            return AutocompleteResponse.from_hits(result["hits"]["hits"], "item")

        suggestion = result["suggest"]["spell-suggestion"][0]["options"]
        if len(suggestion) > 0:
            return AutocompleteResponse.from_suggestion(suggestion)

        return AutocompleteResponse(suggestion=[])
