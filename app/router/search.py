from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.router.dependency.dependencies import get_es_client, get_search_service

router = APIRouter(tags=["search"])


@router.get("/search")
async def search(
    es_client=Depends(get_es_client),
    search_service=Depends(get_search_service),
):
    result = await search_service.search(es_client)
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


search_router = router
