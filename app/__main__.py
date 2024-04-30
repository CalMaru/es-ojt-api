from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.container import AppContainer
from app.core.exception.exception_handler import base_exception_handler
from app.router.category import category_router
from app.router.provider import provider_router


def create_app():
    app = FastAPI(title="es-ojt", version="0.1", root_path="/api/v1")

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

    app.include_router(category_router)
    app.include_router(provider_router)

    base_exception_handler(app)

    @app.on_event("startup")
    async def handle_startup():
        await container.ESClient().connect()

    @app.on_event("shutdown")
    async def handle_shutdown():
        await container.ESClient().close()

    return app


es_app = create_app()
