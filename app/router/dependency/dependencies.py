from fastapi import Request

from app.elastic_search.client import AsyncElasticsearchClient
from app.service.autocomplete_service import AutocompleteService
from app.service.option_service import OptionService
from app.service.search_service import SearchService


def get_es_client(req: Request) -> AsyncElasticsearchClient:
    return req.app.state.es_client


def get_option_service(req: Request) -> OptionService:
    return req.app.container.OptionService()


def get_search_service(req: Request) -> SearchService:
    return req.app.container.SearchService()


def get_autocomplete_service(req: Request) -> AutocompleteService:
    return req.app.container.AutocompleteService()
