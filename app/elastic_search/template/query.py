from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel


class NestedQuery(BaseModel):
    path: str
    terms: Optional[list[dict]]

    @property
    def query(self) -> Union[dict, None]:
        if self.terms is None:
            return None

        return {
            "nested": {
                "path": self.path,
                "query": {
                    "bool": {
                        "must": [{"term": term} for term in self.terms],
                    },
                },
            }
        }


class BoolShouldQuery(BaseModel):
    field: str
    terms: Optional[list[str]]

    @property
    def query(self) -> Union[dict, None]:
        if self.terms is None:
            return None

        return {
            "bool": {
                "should": [{"term": {self.field: term}} for term in self.terms],
            },
        }


class RangeDateQuery(BaseModel):
    start: Optional[datetime]
    end: Optional[datetime]

    @property
    def query(self) -> Union[dict, None]:
        if self.start is None or self.end is None:
            return None

        return {
            "range": {
                "date": {
                    "format": "yyyy-MM-dd",
                    "gte": self.start.strftime("%Y-%m-%d"),
                    "lte": self.end.strftime("%Y-%m-%d"),
                },
            }
        }


class NewsKeywordSearchQuery(BaseModel):
    keyword: str

    @property
    def query(self) -> Union[dict, None]:
        return [{"prefix": {"title"}}]
