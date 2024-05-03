from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, model_validator

from app.core.exception.exception import BadRequestError
from app.core.status_code import StatusCode
from app.model.dto.news_dto import News
from app.model.enum.category_enum import CategoryType
from app.model.enum.provider_enum import ProviderType


class SearchRequest(BaseModel):
    query: str
    reporter: Optional[str]
    start_date: datetime
    end_date: datetime
    category_type: str
    category_name: Optional[str]
    provider_type: str
    provider_name: Optional[str]

    @property
    def params(self) -> dict:
        return {}

    @model_validator(mode="after")
    def validate_date(self):
        system_start_date = datetime.strptime("2021-01-01", "%Y-%m-%d")
        system_end_date = datetime.strptime("2021-09-30", "%Y-%m-%d")

        if self.start_date < system_start_date:
            raise BadRequestError(StatusCode.C21001)

        if self.end_date > system_end_date:
            raise BadRequestError(StatusCode.C21002)

        return self

    @model_validator(mode="after")
    def validate_options(self):
        if CategoryType.has_key(self.category_type) is False:
            raise BadRequestError(StatusCode.C21003)

        if ProviderType.has_key(self.provider_type) is False:
            raise BadRequestError(StatusCode.C21004)

        return self

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
            category_type=category_type,
            category_name=category_name,
            provider_type=provider_type,
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
