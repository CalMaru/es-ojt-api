from enum import auto

from app.elastic_search.config import StrEnum


class Index(StrEnum):
    CATEGORY = "cal-category"
    PROVIDER = "cal-provider"
    REPORTER = "cal-reporter"
    KEYWORD = "cal-keyword"
    NEWS = "cal-news"
