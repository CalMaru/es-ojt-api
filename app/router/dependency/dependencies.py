from fastapi import Request

from app.elastic_search.client import AsyncESClient
from app.service.category_service import CategoryService
from app.service.provider_service import ProviderService


def get_es_client(req: Request) -> AsyncESClient:
    return req.app.container.AsyncESClient()


def get_category_service(req: Request) -> CategoryService:
    return req.app.container.CategoryService()


def get_provider_service(req: Request) -> ProviderService:
    return req.app.container.ProviderService()
