from app.elastic_search.client import AsyncElasticsearchClient
from app.router.dto.autocomplete import AutocompleteResponse
from app.service.autocomplete_service import AutocompleteService


class AutocompleteServiceImpl(AutocompleteService):
    async def get_reporters(
        self,
        query: str,
        es_client: AsyncElasticsearchClient,
    ) -> AutocompleteResponse:
        result = ["a", "b"]
        return AutocompleteResponse(suggestions=result)
