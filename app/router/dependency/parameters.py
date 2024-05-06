from fastapi import Query

from app.router.dto.search import SearchQueryRequest


def get_search_parameters(
    query: str = Query(),
    reporter: str = Query(None),
    start_date: str = Query(None),
    end_date: str = Query(None),
    category_type: str = Query(),
    category_name: str = Query(None),
    provider_type: str = Query(),
    provider_name: str = Query(None),
) -> SearchQueryRequest:
    return SearchQueryRequest.from_request(
        query=query,
        reporter=reporter,
        start_date=start_date,
        end_date=end_date,
        category_type=category_type,
        category_name=category_name,
        provider_type=provider_type,
        provider_name=provider_name,
    )
