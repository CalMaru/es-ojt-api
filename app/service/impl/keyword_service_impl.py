import hgtk
from gksdudaovld import KoEngMapper

from app.elastic_search.client import AsyncElasticsearchClient
from app.elastic_search.config.index import Index
from app.elastic_search.config.template import Autocomplete
from app.model.dto.autocomplete_dto import AutocompleteResponse
from app.service.keyword_service import KeywordService


class KeywordServiceImpl(KeywordService):
    async def autocomplete(
        self,
        query: str,
        key: str,
        index: Index,
        es_client: AsyncElasticsearchClient,
    ) -> AutocompleteResponse:
        if hgtk.checker.is_hangul(query) is False:
            query = KoEngMapper.conv_en2ko(query)

        template = Autocomplete.from_query(query, key)
        result = await es_client.search_template(template, index)

        count = result["hits"]["total"]["value"]
        if count > 0:
            return AutocompleteResponse.from_hits(result["hits"]["hits"], key)

        suggestion = result["suggest"]["spell-suggestion"][0]["options"]
        if len(suggestion) > 0:
            return AutocompleteResponse.from_suggestion(suggestion)

        return AutocompleteResponse(suggestions=[])

    async def is_terms_exist(self, query: str, es_client: AsyncElasticsearchClient):
        template = Autocomplete.from_query(query, "item")
        result = await es_client.search_template(template, Index.KEYWORD)
        return result["hits"]["total"]["value"] > 0
