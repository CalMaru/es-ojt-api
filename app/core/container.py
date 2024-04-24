from dependency_injector import containers, providers

from app.core.config import env_config
from app.elastic_search.engine.client import AsyncESClient
from app.service.impl.autocomplete_service_impl import AutocompleteServiceImpl
from app.service.impl.search_service_impl import SearchServiceImpl
from app.storage.storage_impl.csv_storage_impl import CSVStorageImpl


class AppContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["app"])

    config = providers.Configuration()
    config.from_dict(env_config.model_dump())

    ESClient = providers.Singleton(AsyncESClient)

    CSVStorage = providers.Singleton(
        CSVStorageImpl,
    )

    AutocompleteService = providers.Singleton(
        AutocompleteServiceImpl,
    )

    SearchService = providers.Singleton(
        SearchServiceImpl,
        csv_storage=CSVStorage,
    )
