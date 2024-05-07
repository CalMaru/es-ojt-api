from enum import auto

from app.model import StrEnum


class ProviderType(StrEnum):
    ALL = auto()
    CATEGORY = auto()
    DETAIL = auto()
    LOCAL = auto()
    ALPHABETIC = auto()
