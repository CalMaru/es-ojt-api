from collections import defaultdict
from os.path import join

import pandas as pd

from app.core.config import env_config
from app.model.enum.provider_enum import ProviderType
from app.service.search_service import SearchService
from app.storage.storage_impl.csv_storage_impl import CSVStorageImpl


class SearchServiceImpl(SearchService):
    def __init__(
        self,
        csv_storage: CSVStorageImpl,
    ):
        self.csv_storage = csv_storage

    def get_providers(self, provider_type: ProviderType):
        data_path = env_config.DATA_PATH
        provider_df = self.csv_storage.read_csv(join(data_path, "providers.csv"))

        if provider_type == ProviderType.CATEGORY:
            return list(provider_df["분류"].dropna().unique())
        elif provider_type == ProviderType.DETAIL:
            return self.get_providers_by_column_name(provider_df, "분류")
        elif provider_type == ProviderType.LOCAL:
            return self.get_providers_by_column_name(provider_df, "지역", True)
        elif provider_type == ProviderType.ALPHABETIC:
            pass

    @staticmethod
    def get_providers_by_column_name(provider_df: pd.DataFrame, column_name: str, sort: bool = False) -> dict:
        providers = defaultdict(list)
        categories = list(provider_df[column_name].dropna().unique())

        if sort:
            categories = sorted(categories)

        for category in categories:
            names = provider_df.loc[provider_df[column_name] == category]["이름"]
            providers[category] = sorted(list(names))

        return providers

    @staticmethod
    def get_providers_by_alphabetic_order(provider_df: pd.DataFrame):
        aa = ["ㄱ", "ㄴ", "ㄷ", "ㄹ", "ㅁ", "ㅂ", "ㅅ", "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]

        return None
