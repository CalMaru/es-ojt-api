from enum import auto

from app.elastic_search.config import StrEnum


class ProviderType(StrEnum):
    ALL = auto()
    CATEGORY = auto()
    DETAIL = auto()
    LOCAL = auto()
    ALPHABETIC = auto()
