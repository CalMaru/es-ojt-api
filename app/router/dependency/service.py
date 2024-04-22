from fastapi import Request

from app.service.search_service import SearchService


def get_search_service(req: Request) -> SearchService:
    return req.app.container.SearchService()
