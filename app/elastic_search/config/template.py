from enum import Enum
from typing import Optional

from pydantic import BaseModel

from app.router.dto.search import SearchRequest


class TemplateName(Enum):
    GET_UNIQUE_FIELDS = "get_unique_fields"
    GET_ALL_ITEMS = "get_all_template"
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


class GetUniqueFields(Template):
    @classmethod
    def from_field(cls, field: str):
        return cls(
            id=TemplateName.GET_UNIQUE_FIELDS,
            params={"field": field},
        )


class GetAllItems(Template):
    @classmethod
    def from_null(cls):
        return cls(id=TemplateName.GET_ALL_ITEMS)


class SearchNews(Template):
    @classmethod
    def from_request(cls, request: SearchRequest):
        return cls(
            id=TemplateName.SEARCH_NEWS,
            params=request.params,
        )
