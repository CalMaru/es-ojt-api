from app.model.enum.autocomplete import AutocompleteType
from app.service.autocomplete_service import AutocompleteService


class AutocompleteServiceImpl(AutocompleteService):
    def autocomplete(self, query: str, query_type: AutocompleteType):
        pass
