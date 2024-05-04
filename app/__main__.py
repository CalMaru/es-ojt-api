from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.container import AppContainer
from app.core.exception.exception_handler import base_exception_handler
from app.core.middleware import middleware_handler
from app.elastic_search.client import AsyncElasticsearchClient
from app.router.autocomplete import autocomplete_router
from app.router.option import option_router
from app.router.search import search_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.es_client = AsyncElasticsearchClient()
    yield
    await app.state.es_client.close()


def create_app():
    app = FastAPI(title="es-ojt-api", version="0.1", root_path="/api/v1", lifespan=lifespan)

    container = AppContainer()
    container.wire(packages=["app"])

    app.container = container

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(option_router)
    app.include_router(search_router)
    app.include_router(autocomplete_router)

    base_exception_handler(app)

    middleware_handler(app)

    return app


es_app = create_app()
