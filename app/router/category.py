from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.router.dependency.dependencies import get_category_service, get_es_client

router = APIRouter(tags=["category"])


@router.get("/category")
async def get_categories(
    es_client=Depends(get_es_client),
    category_service=Depends(get_category_service),
):
    result = await category_service.get_categories(es_client)
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


category_router = router
