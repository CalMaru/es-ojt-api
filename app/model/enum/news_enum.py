from enum import auto

from app.model import StrEnum


class NewsField(StrEnum):
    NEWS_ID = auto()
    TITLE = auto()
    CONTENT = auto()
    PROVIDER = auto()
    CATEGORY = auto()
    REPORTER = auto()
    DATE = auto()

    @classmethod
    def list(cls):
        return [c for c in cls]


class NewsSort(StrEnum):
    SCORE = auto()
    LATEST = auto()
    OLD = auto()


class HighlightTag(StrEnum):
    STRONG = auto()
    EM = auto()
    B = auto()
    FONT = auto()
