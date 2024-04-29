from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.router.dependency.dependencies import get_category_service

router = APIRouter(tags=["category"])


@router.get("/category")
async def get_categories(category_service=Depends(get_category_service)):
    result = await category_service.get_categories()
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


category_router = router
