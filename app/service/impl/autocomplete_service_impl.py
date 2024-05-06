import hgtk

from app.elastic_search.client import AsyncElasticsearchClient
from app.elastic_search.config.index import Index
from app.elastic_search.config.parameter import AutocompleteParams
from app.elastic_search.config.template import Autocomplete
from app.router.dto.autocomplete import AutocompleteResponse
from app.service.autocomplete_service import AutocompleteService


class AutocompleteServiceImpl(AutocompleteService):
    async def get_reporters(
        self,
        query: str,
        es_client: AsyncElasticsearchClient,
    ) -> AutocompleteResponse:
        query_jamo = hgtk.text.decompose(query, compose_code="")
        params = AutocompleteParams.from_reporter(query, query_jamo)
        template = Autocomplete.from_params(params)

        result = await es_client.search_template(template, Index.REPORTER)
        return AutocompleteResponse.from_hits(result["hits"]["hits"])
