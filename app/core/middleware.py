from elasticsearch.exceptions import ElasticsearchException, ImproperlyConfigured
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from app.core.status_code import StatusCode


def middleware_handler(app: FastAPI):
    @app.middleware("http")
    async def request_middleware(request: Request, call_next) -> JSONResponse:
        try:
            response = await call_next(request)
        except ImproperlyConfigured:
            return JSONResponse(content=StatusCode.C50001.response(), status_code=500)
        except ElasticsearchException:
            return JSONResponse(content=StatusCode.C50001.response(), status_code=500)
        except Exception:
            return JSONResponse(content=StatusCode.C50000.response(), status_code=500)
        return response
