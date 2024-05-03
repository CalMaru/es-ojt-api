from fastapi import Request

from app.elastic_search.client import AsyncElasticsearchClient
from app.service.option_service import OptionService


def get_es_client(req: Request) -> AsyncElasticsearchClient:
    return req.app.state.es_client


def get_option_service(req: Request) -> OptionService:
    return req.app.container.OptionService()
