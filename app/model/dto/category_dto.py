from collections import OrderedDict, defaultdict

from pydantic import BaseModel


class CategoryType(BaseModel):
    type: str

    @classmethod
    def from_type(cls, type: str):
        return cls(type=type)


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


class NewsCategories(BaseModel):
    """뉴스 유형별 리스트
    Args
        all (str): 전체
        category (:obj:`list[str]`): 유형별 분류
        detail (:obj:`list[Category]`): 유형별 상세 분류
        # alphabetic () : 가나다순
    """

    all: str
    category: list[str]
    detail: dict
    # alphabetic: dict

    @classmethod
    def from_categories(cls, categories: Categories):
        return cls(
            all="전체",
            category=categories.majors,
            detail=categories.detail,
        )
