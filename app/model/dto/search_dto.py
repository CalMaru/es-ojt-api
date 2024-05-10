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

    @classmethod
    def from_requests(cls, start_tag: str, end_tag: str):
        if start_tag is None or end_tag is None:
            return None

        return cls(
            start_tag=start_tag,
            end_tag=end_tag,
        )


class News(BaseModel):
    news_id: Optional[int]
    title: Optional[str]
    content: Optional[str]
    provider: Optional[Provider]
    category: Optional[list[NewsCategory]]
    reporter: Optional[list[str]]
    date: Optional[str]

    @classmethod
    def from_hit(cls, hit: dict, highlight: Optional[Highlight]):
        source = hit["_source"]
        hit_highlight = hit.get("highlight", {})

        title = hit_highlight.get("title", source.get("title", None))
        content = hit_highlight.get("content", source.get("content", None))

        if highlight:
            start_tag, end_tag = highlight.start_tag, highlight.end_tag
            for query in highlight.query.split(" "):
                content = content.replace(query, f"{start_tag}{query}{end_tag}")

        categories = [NewsCategory.from_dict(category) for category in source.get("category", [])]

        reporter = source.get("reporter", None)
        if isinstance(reporter, str):
            reporter = [reporter]

        return cls(
            news_id=source.get("id", None),
            title=title,
            content=content,
            provider=Provider.from_source(source.get("provider", None)),
            category=categories if len(categories) > 0 else None,
            reporter=reporter,
            date=source.get("date", None),
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
    sort_key: str
    sort_value: str
    size: int
    pit_id: Optional[str]
    search_after: Optional[list[T]]
    source: list[NewsField]
    search_alternative: bool
    start_tag: Optional[str]
    end_tag: Optional[str]

    @property
    def sources(self) -> list[str]:
        return [source.field for source in self.source]

    @property
    def category(self) -> Union[list[dict], None]:
        category = []
        if self.category_major:
            category.append({"category.major": self.category_major})
        if self.category_minor:
            category.append({"category.minor": self.category_major})
        return category if len(category) > 0 else None

    @property
    def provider(self) -> Union[list[dict], None]:
        provider = []
        if self.provider_type:
            provider.append({"provider.type": self.provider_type})
        if self.provider_location:
            provider.append({"provider.location": self.provider_location})
        if self.provider_name:
            provider.append({"provider.name": self.provider_name})
        return provider if len(provider) > 0 else None

    @property
    def using_highlight(self) -> bool:
        return self.start_tag is not None and self.end_tag is not None

    @classmethod
    def from_requests(
        cls,
        request: SearchQueryRequest,
        es_request: SearchElasticsearchRequest,
    ):
        highlight = es_request.highlight
        return cls(
            query=request.query,
            reporter=request.reporter,
            start_date=request.start_date,
            end_date=request.end_date,
            category_major=request.category_major,
            category_minor=request.category_minor,
            provider_type=request.provider_type,
            provider_location=request.provider_location,
            provider_name=request.provider_name,
            sort_key=request.sorting.get_key(),
            sort_value=request.sorting.get_value(),
            size=es_request.size,
            pit_id=es_request.pit_id,
            search_after=es_request.search_after,
            source=es_request.source,
            search_alternative=es_request.search_alternative,
            start_tag=highlight.start_tag if highlight is not None else None,
            end_tag=highlight.end_tag if highlight is not None else None,
        )


class SearchResponse(BaseModel):
    pit_id: str
    count: int
    news: list[News]
    search_after: Optional[list[T]]
    alternative: Optional[str]

    @classmethod
    def from_result(cls, result: dict, alternative: Optional[str], request: SearchRequest):
        news, search_after, highlight = [], None, Highlight.from_requests(request.start_tag, request.end_tag)

        for hit in result["hits"]["hits"]:
            news.append(News.from_hit(hit, highlight))

        if len(news) > 0:
            search_after = result["hits"]["hits"][-1].get("sort", None)

        return cls(
            pit_id=request.pit_id,
            count=result["hits"]["total"]["value"],
            news=news,
            search_after=search_after,
            alternative=alternative,
        )
