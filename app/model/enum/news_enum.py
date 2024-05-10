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

    @property
    def field(self) -> str:
        if self.name == NewsField.NEWS_ID:
            return "id"
        return self.name.lower()

    @classmethod
    def list(cls):
        return [c for c in cls]


class NewsSort(StrEnum):
    SCORE = auto()
    LATEST = auto()
    OLD = auto()

    def get_key(self) -> str:
        if self.name == NewsSort.SCORE:
            return "_score"
        return "date"

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
