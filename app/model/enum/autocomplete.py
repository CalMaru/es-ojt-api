from enum import auto

from app.model.enum import StrEnum


class AutocompleteType(StrEnum):
    PROVIDER = auto()
    REPORTER = auto()
