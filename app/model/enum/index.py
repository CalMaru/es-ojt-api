from enum import auto

from app.model.enum import StrEnum


class Index(StrEnum):
    CATEGORY = auto()
    PROVIDER = auto()
    NEWS = auto()
    REPORTER = auto()
