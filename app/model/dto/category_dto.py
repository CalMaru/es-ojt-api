from collections import defaultdict

from pydantic import BaseModel


class Category(BaseModel):
    major: str
    minor: str


class NewsCategories(BaseModel):
    all: str
    category: list[str]
    detail: dict
    # alphabetic: dict

    @classmethod
    def from_categories(cls, majors: list[str], categories: list[Category]):
        majors.sort()

        detail = defaultdict(list)
        for category in categories:
            detail[category.major].append(category.minor)

        for major in detail.keys():
            detail[major].sort()

        return cls(
            all="all",
            category=majors,
            detail=detail,
        )
