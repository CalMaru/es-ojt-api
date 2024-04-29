from fastapi import Request
from starlette.responses import JSONResponse

from app.core.exception.exception import BaseError


def base_exception_handler(app):
    @app.exception_handler(BaseError)
    async def base_error(request: Request, exc: BaseError):
        return JSONResponse(content=exc.response, status_code=exc.status_code)
