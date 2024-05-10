from app.elastic_search.client import AsyncElasticsearchClient
from app.elastic_search.config.index import Index
from app.elastic_search.template.template import GetAllItems
from app.model.dto.category_dto import Categories, NewsCategories
from app.model.dto.option_dto import GetOptionsResponse
from app.model.dto.provider_dto import NewsProviders, Providers
from app.service.option_service import OptionService


class OptionServiceImpl(OptionService):
    async def get_options(self, es_client: AsyncElasticsearchClient) -> GetOptionsResponse:
        categories = await self.get_all_categories(es_client)
        news_categories = NewsCategories.from_categories(categories)

        providers = await self.get_all_providers(es_client)
        news_providers = NewsProviders.from_providers(providers)

        return GetOptionsResponse.from_options(news_categories, news_providers)

    @staticmethod
    async def get_all_categories(es_client: AsyncElasticsearchClient) -> Categories:
        result = await es_client.search_template(GetAllItems.from_null(), Index.CATEGORY)
        return Categories.from_hits(result["hits"]["hits"])

    @staticmethod
    async def get_all_providers(es_client: AsyncElasticsearchClient) -> Providers:
        result = await es_client.search_template(GetAllItems.from_null(), Index.PROVIDER)
        return Providers.from_hits(result["hits"]["hits"])
