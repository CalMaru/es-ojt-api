from collections import OrderedDict, defaultdict
from typing import Optional

import hgtk
from pydantic import BaseModel

from app.elastic_search.config.hangeul import Hangeul


class Provider(BaseModel):
    name: str
    type: str
    location: Optional[str]

    @classmethod
    def from_source(cls, provider: dict):
        if provider is None:
            return None

        return cls(
            name=provider["name"],
            type=provider["type"],
            location=provider.get("location", None),
        )


class Providers(BaseModel):
    providers: list[Provider]

    @classmethod
    def from_hits(cls, hits: dict):
        providers = []
        for hit in hits:
            providers.append(Provider.from_source(hit["_source"]))

        return cls(providers=providers)

    @property
    def category(self) -> list[str]:
        types = set()
        for provider in self.providers:
            types.add(provider.type)

        types = list(types)
        types.sort()
        return types

    @property
    def detail(self) -> dict:
        detail = defaultdict(list)
        for provider in self.providers:
            detail[provider.type].append(provider.name)

        for provider_type in detail.keys():
            detail[provider_type].sort()

        return detail

    @property
    def local(self) -> dict:
        local = defaultdict(list)
        for provider in self.providers:
            if provider.location:
                local[provider.location].append(provider.name)

        local = OrderedDict(sorted(local.items()))
        for location in local.keys():
            local[location].sort()

        return local

    @property
    def alphabetic(self) -> dict:
        alphabetic = defaultdict(list)
        jaeums, english = Hangeul.JAEUMS.value, "abc"
        for provider in self.providers:
            first_jaeum = hgtk.text.decompose(provider.name)[0]
            if first_jaeum in jaeums:
                alphabetic[first_jaeum].append(provider.name)
            else:
                alphabetic[english].append(provider.name)

        alphabetic = OrderedDict(sorted(alphabetic.items()))
        for name in alphabetic.keys():
            alphabetic[name].sort()

        return alphabetic


class NewsProviders(BaseModel):
    """언론사 유형별 리스트
    Args
        all (str): 전체
        category (:obj:`list[str]`): 유형별
        detail (dict): 언론사 분류순
        local (dict): 지역별 언론사
        alphabetic (dict) : 가나다순
    """

    all: str
    category: list[str]
    detail: dict
    local: dict
    alphabetic: dict

    @classmethod
    def from_providers(cls, providers: Providers):
        return cls(
            all="전체",
            category=providers.category,
            detail=providers.detail,
            local=providers.local,
            alphabetic=providers.alphabetic,
        )
