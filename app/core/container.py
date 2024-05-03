from dependency_injector import containers, providers

from app.core.config import env_config
from app.service.impl.option_service_impl import OptionServiceImpl
from app.service.impl.search_service_impl import SearchServiceImpl


class AppContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["app"])

    config = providers.Configuration()
    config.from_dict(env_config.model_dump())

    OptionService = providers.Singleton(
        OptionServiceImpl,
    )

    SearchService = providers.Singleton(
        SearchServiceImpl,
    )
