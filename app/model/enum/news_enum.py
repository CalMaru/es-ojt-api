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

    def get_key(self) -> str:
        return self.name.lower()

    def get_value(self) -> str:
        if self.name == NewsSort.SCORE:
            return "desc"
        elif self.name == NewsSort.LATEST:
            return "desc"
        return "asc"


class HighlightTag(StrEnum):
    STRONG = auto()
    EM = auto()
    B = auto()
    FONT = auto()
