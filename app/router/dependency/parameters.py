from fastapi import Query

from app.model.dto.search_dto import SearchQueryRequest


def get_search_parameters(
    query: str = Query(),
    reporter: str = Query(None),
    start_date: str = Query(None),
    end_date: str = Query(None),
    category_major: str = Query(None),
    category_minor: str = Query(None),
    provider_type: str = Query(None),
    provider_location: str = Query(None),
    provider_name: str = Query(None),
    sorting: str = Query(None),
) -> SearchQueryRequest:
    return SearchQueryRequest.from_request(
        query=query,
        reporter=reporter,
        start_date=start_date,
        end_date=end_date,
        category_major=category_major,
        category_minor=category_minor,
        provider_type=provider_type,
        provider_location=provider_location,
        provider_name=provider_name,
        sorting=sorting,
    )
