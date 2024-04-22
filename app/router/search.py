from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.router.dependency.service import get_search_service

router = APIRouter(tags=["search"])


@router.get("/search/test")
def test(search_service=Depends(get_search_service)):
    result = {"result": "app"}
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


search_router = router
