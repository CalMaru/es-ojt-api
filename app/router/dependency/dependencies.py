from fastapi import Request

from app.elastic_search.engine.client import AsyncESClient
from app.service.search_service import SearchService


def get_es_client(req: Request) -> AsyncESClient:
    return req.app.container.AsyncESClient()


def get_autocomplete_service(req: Request) -> SearchService:
    return req.app.container.AutocompleteService()


def get_search_service(req: Request) -> SearchService:
    return req.app.container.SearchService()
