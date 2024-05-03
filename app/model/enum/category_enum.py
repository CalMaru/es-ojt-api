from enum import auto

from app.elastic_search.config import StrEnum


class CategoryType(StrEnum):
    ALL = auto()
    CATEGORY = auto()
    DETAIL = auto()
    ALPHABETIC = auto()
