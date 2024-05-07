from enum import auto

from app.model import StrEnum


class CategoryType(StrEnum):
    ALL = auto()
    CATEGORY = auto()
    DETAIL = auto()
    ALPHABETIC = auto()
