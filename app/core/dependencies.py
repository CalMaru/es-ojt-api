from fastapi import Request

from app.elasticsearch.elasticsearch import ESClient
from app.service.search_service import SearchService


def get_es_client(req: Request) -> ESClient:
    return req.app.container.ESClient()


def get_search_service(req: Request) -> SearchService:
    return req.app.container.SearchService()
