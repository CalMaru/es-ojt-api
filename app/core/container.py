from dependency_injector import containers, providers

from app.core.config import env_config
from app.elastic_search.client import AsyncESClient
from app.service.impl.category_service_impl import CategoryServiceImpl
from app.service.impl.provider_service_impl import ProviderServiceImpl


class AppContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["app"])

    config = providers.Configuration()
    config.from_dict(env_config.model_dump())

    ESClient = providers.Singleton(AsyncESClient)

    CategoryService = providers.Singleton(
        CategoryServiceImpl,
        es_client=ESClient,
    )

    ProviderService = providers.Singleton(
        ProviderServiceImpl,
        es_client=ESClient,
    )
