from collections import OrderedDict, defaultdict

import hgtk
from pydantic import BaseModel

from app.elastic_search.config.hangeul import Hangeul


class NewsCategory(BaseModel):
    major: str
    minor: str

    @classmethod
    def from_dict(cls, category: dict):
        return cls(
            major=category["major"],
            minor=category["minor"],
        )


class Category(BaseModel):
    major: str
    minors: list[str]

    @classmethod
    def from_all(cls, major: str, minors: list[str]):
        return cls(
            major=major,
            minors=minors,
        )


class Categories(BaseModel):
    categories: list[Category]

    @classmethod
    def from_hits(cls, hits: dict):
        categories = defaultdict(list)
        for hit in hits:
            category = hit["_source"]
            categories[category["major"]].append(category["minor"])

        categories = OrderedDict(sorted(categories.items()))
        for major in categories.keys():
            categories[major].sort()

        categories = [Category.from_all(major, minors) for major, minors in categories.items()]
        return cls(categories=categories)

    @property
    def majors(self) -> list[str]:
        return [category.major for category in self.categories]

    @property
    def detail(self) -> dict:
        detail = defaultdict(list)
        for category in self.categories:
            detail[category.major] = category.minors
        return detail

    @property
    def alphabetic(self) -> dict:
        alphabetic = defaultdict(list)
        jaeums, english = Hangeul.JAEUMS.value, "abc"
        for category in self.categories:
            for minor in category.minors:
                first_jaeum = hgtk.text.decompose(minor)[0]
                if first_jaeum in jaeums:
                    alphabetic[first_jaeum].append(minor)
                else:
                    alphabetic[english].append(minor)

        alphabetic = OrderedDict(sorted(alphabetic.items()))
        for major in alphabetic.keys():
            alphabetic[major].sort()

        return alphabetic


class NewsCategories(BaseModel):
    """뉴스 유형별 리스트
    Args
        all (str): 전체
        category (:obj:`list[str]`): 유형별 분류
        detail (dict): 유형별 상세 분류
        alphabetic (dict) : 가나다순
    """

    all: str
    category: list[str]
    detail: dict
    alphabetic: dict

    @classmethod
    def from_categories(cls, categories: Categories):
        return cls(
            all="전체",
            category=categories.majors,
            detail=categories.detail,
            alphabetic=categories.alphabetic,
        )
