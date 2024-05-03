from app.elastic_search.client import AsyncElasticsearchClient
from app.model.dto.category_dto import Category, NewsCategories
from app.model.enum.index import Index
from app.service.option_service import OptionService


class OptionServiceImpl(OptionService):
    async def get_options(self, es_client: AsyncElasticsearchClient):
        get_unique_categories_body = {"id": "get_unique_fields", "params": {"field": "major"}}

        get_all_body = {"id": "get_all_template"}

        result = await es_client.search_template(get_unique_categories_body, Index.CATEGORY)
        buckets = result["aggregations"]["unique_fields"]["buckets"]
        majors = [bucket["key"] for bucket in buckets]

        category_result = await es_client.search_template(get_all_body, Index.CATEGORY)
        categories = [Category(**hit["_source"]) for hit in category_result["hits"]["hits"]]

        news_categories = NewsCategories.from_categories(majors, categories)
        return news_categories

        # alphabetic_body = await es_client.search()

        # provider_body = {"id": "get_providers_template"}
        # provider_result = await es_client.search(body, Index.PROVIDER)
        # providers = [Provider(**hit["_source"]) for hit in provider_result["hits"]["hits"]]
