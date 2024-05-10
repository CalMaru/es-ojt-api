from typing import Optional

import hgtk
from pydantic import BaseModel

from app.elastic_search.config import StrEnum
from app.elastic_search.template.query import BoolShouldQuery, NestedQuery, RangeDateQuery
from app.model.dto.search_dto import SearchRequest


class TemplateName(StrEnum):
    GET_ALL_ITEMS = "get_all_items"
    AUTOCOMPLETE = "autocomplete"
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


class Autocomplete(Template):
    @classmethod
    def from_query(cls, query: str, key: str):
        query_jamo = hgtk.text.decompose(query, compose_code="")
        return cls(
            id=TemplateName.AUTOCOMPLETE,
            params={
                "key": key,
                "query": query,
                "query_jamo": query_jamo,
            },
        )


class SearchNews(Template):
    @classmethod
    def from_request(cls, request: SearchRequest):
        category = NestedQuery(path="category", terms=request.category).query
        provider = NestedQuery(path="provider", terms=request.provider).query
        reporter = BoolShouldQuery(terms=request.reporter).query
        date = RangeDateQuery(start=request.start_date, end=request.end_date).query

        must = []
        for item in (category, provider, reporter, date):
            if item is not None:
                must.append(item)

        return cls(
            id=TemplateName.SEARCH_NEWS,
            params={
                "size": request.size,
                "pit_id": request.pit_id,
                "page": True if request.search_after else False,
                "search_after": request.search_after,
                "source": request.sources,
                "must": must,
                "query": request.query,
                "sort_key": request.sort_key,
                "sort_value": request.sort_value,
                "highlight": request.using_highlight,
                "start_tag": request.start_tag,
                "end_tag": request.end_tag,
            },
        )
