from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.core.dependencies import get_search_service
from app.model.enum.provider_enum import ProviderType

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
