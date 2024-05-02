from dependency_injector import containers, providers

from app.core.config import env_config
from app.service.impl.category_service_impl import CategoryServiceImpl


class AppContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["app"])

    config = providers.Configuration()
    config.from_dict(env_config.model_dump())

    CategoryService = providers.Singleton(
        CategoryServiceImpl,
    )
