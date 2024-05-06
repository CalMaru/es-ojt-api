from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.router.dependency.dependencies import get_es_client, get_search_service
from app.router.dependency.parameters import get_search_parameters
from app.router.dto.search import SearchElasticsearchRequest, SearchQueryRequest, SearchResponse

router = APIRouter(tags=["search"])


@router.get("/search", response_model=SearchResponse)
async def search(
    es_request: SearchElasticsearchRequest,
    query_request: SearchQueryRequest = Depends(get_search_parameters),
    es_client=Depends(get_es_client),
    search_service=Depends(get_search_service),
):
    es_request.initialize()
    result = await search_service.search(query_request, es_request, es_client)
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


search_router = router
