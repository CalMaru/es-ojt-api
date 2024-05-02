from fastapi import Request

from app.elastic_search.client import AsyncElasticsearchClient
from app.service.category_service import CategoryService


def get_es_client(req: Request) -> AsyncElasticsearchClient:
    return req.app.state.es_client


def get_category_service(req: Request) -> CategoryService:
    return req.app.container.CategoryService()
