from enum import auto

from app.elastic_search.config import StrEnum


class Index(StrEnum):
    CATEGORY = auto()
    PROVIDER = auto()
    NEWS = auto()
    REPORTER = auto()
