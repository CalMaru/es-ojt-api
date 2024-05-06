from fastapi import APIRouter, Depends, Query
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.router.dependency.dependencies import get_autocomplete_service, get_es_client
from app.router.dto.autocomplete import AutocompleteResponse

router = APIRouter(tags=["autocomplete"])


@router.get("/autocomplete/reporter", response_model=AutocompleteResponse)
async def autocomplete_reporter(
    query=Query(),
    es_client=Depends(get_es_client),
    autocomplete_service=Depends(get_autocomplete_service),
):
    result = await autocomplete_service.get_reporters(query, es_client)
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


@router.get("/autocomplete/news-keyword", response_model=AutocompleteResponse)
async def autocomplete_news_keyword(
    query=Query(),
    es_client=Depends(get_es_client),
    autocomplete_service=Depends(get_autocomplete_service),
):
    result = await autocomplete_service.get_news_keyword(query, es_client)
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


autocomplete_router = router
