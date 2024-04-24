from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.model.enum.autocomplete import AutocompleteType
from app.router.dependency.dependencies import get_autocomplete_service

router = APIRouter(tags=["autocomplete"])


@router.get("/autocomplete/provider")
def complete_provider(
    query: str,
    autocomplete_service=Depends(get_autocomplete_service),
):
    result = autocomplete_service.autocomplete(query, AutocompleteType.PROVIDER)
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


@router.get("/autocomplete/reporter")
def complete_reporter(
    query: str,
    autocomplete_service=Depends(get_autocomplete_service),
):
    result = autocomplete_service.autocomplete(query, AutocompleteType.REPORTER)
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


autocomplete_router = router
