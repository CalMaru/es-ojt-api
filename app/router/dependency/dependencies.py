from fastapi import Request

from app.elastic_search.client import AsyncESClient
from app.service.category_service import CategoryService
from app.service.provider_service import ProviderService
from app.service.search_service import SearchService


def get_es_client(req: Request) -> AsyncESClient:
    return req.app.container.AsyncESClient()


def get_autocomplete_service(req: Request) -> SearchService:
    return req.app.container.AutocompleteService()


def get_search_service(req: Request) -> SearchService:
    return req.app.container.SearchService()


def get_category_service(req: Request) -> CategoryService:
    return req.app.container.CategoryService()


def get_provider_service(req: Request) -> ProviderService:
    return req.app.container.ProviderService()
