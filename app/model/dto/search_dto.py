from datetime import datetime
from typing import Optional, TypeVar, Union

from pydantic import BaseModel, Field, model_validator

from app.core.exception.exception import BadRequestError
from app.core.status_code import StatusCode
from app.model.dto.category_dto import NewsCategory
from app.model.dto.provider_dto import Provider
from app.model.enum.category_enum import CategoryType
from app.model.enum.news_enum import HighlightTag, NewsField, NewsSort
from app.model.enum.provider_enum import ProviderType

T = TypeVar("T")


class SearchQueryRequest(BaseModel):
    query: str
    reporter: Optional[str]
    start_date: datetime
    end_date: datetime
    category_type: str
    category_name: Optional[str]
    provider_type: str
    provider_name: Optional[str]
    sorting: str

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
    def validate_options(self):
        if CategoryType.has_key(self.category_type) is False:
            raise BadRequestError(StatusCode.C21003, CategoryType.get_description())

        if ProviderType.has_key(self.provider_type) is False:
            raise BadRequestError(StatusCode.C21004, ProviderType.get_description())

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
        category_type: Union[str, None],
        category_name: Union[str, None],
        provider_type: Union[str, None],
        provider_name: Union[str, None],
        sorting: Union[str, None],
    ):
        if start_date is None:
            start_date = "2021-01-01"
        if end_date is None:
            end_date = "2021-09-30"
        if category_type is None:
            category_type = "all"
        if provider_type is None:
            provider_type = "all"
        if sorting is None:
            sorting = "score"

        return cls(
            query=query,
            reporter=reporter,
            start_date=datetime.strptime(start_date, "%Y-%m-%d"),
            end_date=datetime.strptime(end_date, "%Y-%m-%d"),
            category_type=category_type,
            category_name=category_name,
            provider_type=provider_type,
            provider_name=provider_name,
            sorting=sorting,
        )


class SearchElasticsearchRequest(BaseModel):
    size: Optional[int] = Field(None, gt=0)
    pit_id: Optional[str] = Field(None)
    search_after: Optional[list[T]] = Field(None)
    source: Optional[list[NewsField]] = Field(None)
    search_alternative: bool = Field(True)
    highlight_tag: Optional[str] = Field(None)
    highlight_color: Optional[str] = Field(None)

    @model_validator(mode="after")
    def initialize(self):
        if self.size is None:
            self.size = 10
        if self.source is None:
            self.source = NewsField.list()

        return self

    @model_validator(mode="after")
    def validate_highlight(self):
        if self.highlight_tag is None:
            return self
        if HighlightTag.has_key(self.highlight_tag) is False:
            raise BadRequestError(StatusCode.C21006, HighlightTag.get_description())
        return self


class HighlightInfo(BaseModel):
    query: str
    tag: Optional[HighlightTag]
    color: Optional[str]

    @property
    def start_tag(self) -> str:
        if self.tag:
            if self.color:
                return f"<{self.tag.lower()} color={self.color}>"
            return f"<{self.tag.lower()}>"
        return ""

    @property
    def end_tag(self) -> str:
        if self.tag:
            return f"</{self.tag.lower()}>"
        return ""

    @classmethod
    def from_request(cls, query: str, request: SearchElasticsearchRequest):
        tag = request.highlight_tag.upper() if request.highlight_tag is not None else None
        return cls(
            query=query,
            tag=HighlightTag[tag] if tag is not None else None,
            color=request.highlight_color,
        )


class News(BaseModel):
    news_id: Optional[str]
    title: Optional[str]
    content: Optional[str]
    provider: Optional[list[Provider]]
    category: Optional[list[NewsCategory]]
    reporter: Optional[list[str]]
    date: Optional[str]

    @classmethod
    def from_hit(cls, hit: dict, fields: list[NewsField], highlight: HighlightInfo):
        source = hit["_source"]
        hit_highlight = hit.get(hit["highlight"], {})

        title = hit_highlight.get("title", source.get("title", None))
        content = hit_highlight.get("content", source.get("content", None))

        if content and highlight.tag:
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


class SearchRequest(BaseModel):
    query: str
    reporter: Optional[str]
    start_date: datetime
    end_date: datetime
    category_type: CategoryType
    category_name: Optional[str]
    provider_type: ProviderType
    provider_name: Optional[str]
    sorting: NewsSort
    size: int
    pit_id: Optional[str]
    search_after: Optional[list[T]]
    source: list[NewsField]
    search_alternative: bool
    highlight: HighlightInfo

    @property
    def params(self) -> dict:
        return self.dict(exclude_none=True)

    @classmethod
    def from_requests(
        cls,
        request: SearchQueryRequest,
        es_request: SearchElasticsearchRequest,
    ):
        return cls(
            query=request.query,
            reporter=request.reporter,
            start_date=request.start_date,
            end_date=request.end_date,
            category_type=CategoryType[request.category_type.upper()],
            category_name=request.category_name,
            provider_type=ProviderType[request.provider_type.upper()],
            provider_name=request.provider_name,
            sorting=NewsSort[request.sorting.upper()],
            size=es_request.size,
            pit_id=es_request.pit_id,
            search_after=es_request.search_after,
            source=es_request.source,
            search_alternative=es_request.search_alternative,
            highlight=HighlightInfo.from_request(request.query, es_request),
        )


class SearchResponse(BaseModel):
    pit_id: str
    count: int
    news: list[News]
    sort: list[int]

    @classmethod
    def from_result(cls, result: dict, fields: list[NewsField], highlight: HighlightInfo):
        return cls(
            pit_id=result["pit_id"],
            count=result["hits"]["total"]["value"],
            news=[News.from_hit(hit, fields, highlight) for hit in result["hits"]["hits"]],
            sort=result["hits"]["hits"][-1]["sort"],
        )
