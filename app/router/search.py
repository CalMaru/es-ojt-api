from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.model.enum.provider import ProviderType
from app.router.dependency.dependencies import get_search_service

router = APIRouter(tags=["search"])


@router.get("/search/test")
def test(search_service=Depends(get_search_service)):
    result = {"result": "app"}
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


@router.get("/search/providers/{provider_type}")
def providers(
    provider_type: ProviderType,
    search_service=Depends(get_search_service),
):
    result = search_service.get_providers(provider_type)
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


search_router = router
