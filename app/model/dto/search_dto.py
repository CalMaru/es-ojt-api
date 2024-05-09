from datetime import datetime
from typing import Optional, TypeVar, Union

from pydantic import BaseModel, Field, model_validator

from app.core.exception.exception import BadRequestError
from app.core.status_code import StatusCode
from app.model.dto.category_dto import NewsCategory
from app.model.dto.provider_dto import Provider
from app.model.enum.news_enum import NewsField, NewsSort

T = TypeVar("T")


class Highlight(BaseModel):
    start_tag: str
    end_tag: str


class News(BaseModel):
    news_id: Optional[str]
    title: Optional[str]
    content: Optional[str]
    provider: Optional[list[Provider]]
    category: Optional[list[NewsCategory]]
    reporter: Optional[list[str]]
    date: Optional[str]

    @classmethod
    def from_hit(cls, hit: dict, fields: list[NewsField], highlight: Optional[Highlight]):
        source = hit["_source"]
        hit_highlight = hit.get(hit["highlight"], {})

        title = hit_highlight.get("title", source.get("title", None))
        content = hit_highlight.get("content", source.get("content", None))

        if highlight:
            start_tag, end_tag = highlight.start_tag, highlight.end_tag
            for query in highlight.query.split(" "):
                content = content.replace(query, f"{start_tag}{query}{end_tag}")

        if NewsField.PROVIDER in fields:
            providers = [Provider.from_source(provider) for provider in source["provider"]]
        else:
            providers = None

        if NewsField.CATEGORY in fields:
            categories = [NewsCategory.from_source(category) for category in source["category"]]
        else:
            categories = None

        return cls(
            news_id=hit["_id"] if NewsField.NEWS_ID in fields else None,
            title=title if NewsField.TITLE in fields else None,
            content=content if NewsField.CONTENT in fields else None,
            provider=providers,
            category=categories,
            reporter=source["reporter"] if NewsField.REPORTER in fields else None,
            date=source["date"] if NewsField.DATE in fields else None,
        )


class SearchQueryRequest(BaseModel):
    query: str
    reporter: Optional[list[str]]
    start_date: datetime
    end_date: datetime
    category_major: Optional[str]
    category_minor: Optional[str]
    provider_type: Optional[str]
    provider_location: Optional[str]
    provider_name: Optional[str]
    sorting: Union[str, NewsSort]

    @model_validator(mode="after")
    def validate_date(self):
        system_start_date = datetime.strptime("2021-01-01", "%Y-%m-%d")
        system_end_date = datetime.strptime("2021-09-30", "%Y-%m-%d")

        if self.start_date < system_start_date:
            raise BadRequestError(
                StatusCode.C21001,
                "start_date should be greater than 2021-01-01",
            )

        if self.end_date > system_end_date:
            raise BadRequestError(
                StatusCode.C21002,
                "end_date should be less than 2021-09-30",
            )

        return self

    @model_validator(mode="after")
    def validate_sorting(self):
        if NewsSort.has_key(self.sorting) is False:
            raise BadRequestError(StatusCode.C21005, NewsSort.get_description())

        self.sorting = NewsSort[self.sorting.upper()]
        return self

    @classmethod
    def from_request(
        cls,
        query: str,
        reporter: Union[str, None],
        start_date: Union[str, None],
        end_date: Union[str, None],
        category_major: Union[str, None],
        category_minor: Union[str, None],
        provider_type: Union[str, None],
        provider_location: Union[str, None],
        provider_name: Union[str, None],
        sorting: Union[str, None],
    ):
        if isinstance(reporter, str):
            reporter = reporter.split(",")
        if start_date is None:
            start_date = "2021-01-01"
        if end_date is None:
            end_date = "2021-09-30"
        if sorting is None:
            sorting = "score"

        return cls(
            query=query,
            reporter=reporter,
            start_date=datetime.strptime(start_date, "%Y-%m-%d"),
            end_date=datetime.strptime(end_date, "%Y-%m-%d"),
            category_major=category_major,
            category_minor=category_minor,
            provider_type=provider_type,
            provider_location=provider_location,
            provider_name=provider_name,
            sorting=sorting,
        )


class SearchElasticsearchRequest(BaseModel):
    size: Optional[int] = Field(None, gt=0)
    pit_id: Optional[str] = Field(None)
    search_after: Optional[list[T]] = Field(None)
    source: Optional[list[NewsField]] = Field(None)
    search_alternative: Optional[bool] = Field(None)
    highlight: Optional[Highlight] = Field(None)

    @model_validator(mode="after")
    def initialize(self):
        if self.size is None:
            self.size = 10
        if self.source is None:
            self.source = NewsField.list()
        if self.search_alternative is None:
            self.search_alternative = True
        return self


class SearchRequest(BaseModel):
    query: str
    reporter: Optional[list[str]]
    start_date: datetime
    end_date: datetime
    category_major: Optional[str]
    category_minor: Optional[str]
    provider_type: Optional[str]
    provider_location: Optional[str]
    provider_name: Optional[str]
    sorting: NewsSort
    size: int
    pit_id: Optional[str]
    search_after: Optional[list[T]]
    source: list[NewsField]
    search_alternative: bool
    highlight: Optional[Highlight]

    @property
    def params(self) -> dict:
        return self.dict(exclude_none=True)


class SearchResponse(BaseModel):
    pit_id: str
    count: int
    news: list[News]
    search_after: list[T]
    alternative: Optional[str]

    @classmethod
    def from_result(cls, result: dict, alternative: Optional[str], request: SearchRequest):
        news, fields, highlight = [], request.fields, request.highlight
        for hit in result["hits"]["hits"]:
            news.append(News.from_hit(hit, fields, highlight))

        search_after = result["hits"]["hits"][-1]["sort"] if len(news) > 0 else None

        return cls(
            pit_id=result["pit_id"],
            count=result["hits"]["total"]["value"],
            news=news,
            search_after=search_after,
            alternative=alternative,
        )
