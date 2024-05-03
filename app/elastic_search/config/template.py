from enum import Enum
from typing import Optional

from pydantic import BaseModel

from app.elastic_search.config.parameter import AutocompleteParams
from app.router.dto.search import SearchRequest


class TemplateName(Enum):
    GET_ALL_ITEMS = "get_all_template"
    AUTOCOMPLETE = "autocomplete"
    SEARCH_NEWS = "..."


class Template(BaseModel):
    id: TemplateName
    params: Optional[dict] = None

    @property
    def body(self) -> dict:
        body = dict()
        body["id"] = self.id.value
        if self.params:
            body["params"] = self.params
        return body


class GetAllItems(Template):
    @classmethod
    def from_null(cls):
        return cls(id=TemplateName.GET_ALL_ITEMS)


class Autocomplete(Template):
    @classmethod
    def from_params(cls, params: AutocompleteParams):
        return cls(
            id=TemplateName.AUTOCOMPLETE,
            params=params,
        )


class SearchNews(Template):
    @classmethod
    def from_request(cls, request: SearchRequest):
        return cls(
            id=TemplateName.SEARCH_NEWS,
            params=request.params,
        )
