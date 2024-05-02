from collections import defaultdict

from pydantic import BaseModel


class Category(BaseModel):
    major: str
    minor: str


class CategoryDDD(BaseModel):
    all: str
    category: list[str]
    detail: dict[list[str]]
    alphabetic: dict[str]

    @classmethod
    def from_categories(cls, majors: list[str], categories: list[Category]):
        detail = defaultdict(list)
        for category in categories:
            detail[category.major].append(category.minor)

        return cls(
            all="all",
            category=majors,
            detail=detail,
            alphabetic=None,
        )
