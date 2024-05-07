from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.model.dto.option_dto import GetOptionsResponse
from app.router.dependency.dependencies import get_es_client, get_option_service

router = APIRouter(tags=["option"])


@router.get("/option", response_model=GetOptionsResponse)
async def get_options(
    es_client=Depends(get_es_client),
    option_service=Depends(get_option_service),
):
    result = await option_service.get_options(es_client)
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


option_router = router
