from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.router.dependency.dependencies import get_provider_service

router = APIRouter(tags=["provider"])


@router.get("/provider")
async def get_providers(provider_service=Depends(get_provider_service)):
    result = await provider_service.get_providers()
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


provider_router = router
