from app.elastic_search.engine.client import AsyncESClient
from app.service.provider_service import ProviderService


class ProviderServiceImpl(ProviderService):
    def __init__(self, es_client: AsyncESClient):
        self.es_client = es_client

    async def get_providers(self):
        pass
