from enum import Enum
from typing import Optional

import hgtk
from pydantic import BaseModel

from app.model.dto.search_dto import SearchRequest


class TemplateName(Enum):
    GET_ALL_ITEMS = "get_all_items"
    AUTOCOMPLETE_REPORTER = "autocomplete_reporter"
    AUTOCOMPLETE_NEWS_KEYWORD = "autocomplete_news_keyword"
    SEARCH_NEWS = "search_news"


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


class AutocompleteReporter(Template):
    @classmethod
    def from_query(cls, query: str):
        query_jamo = hgtk.text.decompose(query, compose_code="")
        return cls(
            id=TemplateName.AUTOCOMPLETE_REPORTER,
            params={"query": query, "query_jamo": query_jamo},
        )


class AutocompleteNewsKeyword(Template):
    @classmethod
    def from_query(cls, query: str):
        query_jamo = hgtk.text.decompose(query, compose_code="")
        return cls(
            id=TemplateName.AUTOCOMPLETE_NEWS_KEYWORD,
            params={"query": query, "query_jamo": query_jamo},
        )


class SearchNews(Template):
    @classmethod
    def from_request(cls, request: SearchRequest):
        return cls(
            id=TemplateName.SEARCH_NEWS,
            params=request.params,
        )
