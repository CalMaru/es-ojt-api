from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel

from app.model.dto.category_dto import CategoryType
from app.model.dto.news_dto import News
from app.model.dto.provider_dto import ProviderType


class SearchRequest(BaseModel):
    query: str
    reporter: Optional[str]
    start_date: datetime
    end_date: datetime
    category_type: CategoryType
    category_name: Optional[str]
    provider_type: ProviderType
    provider_name: Optional[str]

    @property
    def params(self) -> dict:
        return {}

    @classmethod
    def from_request(
        cls,
        query: str,
        reporter: Union[str, None],
        start_date: Union[str, None],
        end_date: Union[str, None],
        category_type: str,
        category_name: Union[str, None],
        provider_type: str,
        provider_name: Union[str, None],
    ):
        if start_date is None:
            start_date = "2021-01-01"
        if end_date is None:
            end_date = "2021-09-30"

        return cls(
            query=query,
            reporter=reporter,
            start_date=datetime.strptime(start_date, "%Y-%m-%d"),
            end_date=datetime.strptime(end_date, "%Y-%m-%d"),
            category_type=CategoryType.from_type(category_type),
            category_name=category_name,
            provider_type=ProviderType.from_type(provider_type),
            provider_name=provider_name,
        )


class SearchResponse(BaseModel):
    pit_id: str
    count: int
    news: list[News]
    sort: list[int]

    @classmethod
    def from_result(cls, result: dict):
        return cls(
            pit_id=result["pit_id"],
            count=result["hits"]["total"]["value"],
            news=[News.from_hit(hit) for hit in result["hits"]["hits"]],
            sort=result["hits"]["hits"][-1]["sort"],
        )
