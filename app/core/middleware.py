import traceback

from elasticsearch.exceptions import ElasticsearchException, ImproperlyConfigured, NotFoundError
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from app.core.logger.api_logger import app_logger
from app.core.status_code import StatusCode


def middleware_handler(app: FastAPI):
    @app.middleware("http")
    async def request_middleware(request: Request, call_next) -> JSONResponse:
        try:
            response = await call_next(request)
        except ImproperlyConfigured:
            app_logger.error(f"Elasticsearch - ImproperlyConfigured, {traceback.format_exc()}")
            return JSONResponse(content=StatusCode.C50001.response(), status_code=500)
        except NotFoundError as e:
            reason = e.args[2]["error"]["root_cause"][0]["reason"]
            app_logger.error(f"Elasticsearch - NotFoundError, {traceback.format_exc()}")
            return JSONResponse(content=StatusCode.C50002.response(reason), status_code=500)
        except ElasticsearchException:
            app_logger.error(f"Elasticsearch - ElasticsearchException, {traceback.format_exc()}")
            return JSONResponse(content=StatusCode.C50001.response(), status_code=500)
        except Exception:
            app_logger.error(traceback.format_exc())
            return JSONResponse(content=StatusCode.C50000.response(), status_code=500)
        return response
