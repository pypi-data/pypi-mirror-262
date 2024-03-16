# exceptions.py

import sys

from typing import Union

from fastapi import Request
from fastapi.exceptions import (
    RequestValidationError,
    HTTPException,
    WebSocketRequestValidationError,
)
from fastapi.exception_handlers import (
    http_exception_handler as _http_exception_handler,
    request_validation_exception_handler as _request_validation_exception_handler,
    websocket_request_validation_exception_handler as _websocket_request_validation_exception_handler,
)
from fastapi.websockets import WebSocket
from fastapi.responses import JSONResponse, Response
from sqlalchemy.exc import SQLAlchemyError

from api_logger import setup_logger, log_api_error

logger = setup_logger("api_exceptions.log", "api_exceptions")


async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    This is a wrapper to the default RequestValidationException handler of FastAPI.
    This function will be called when client input is not valid.
    """
    logger.debug("Our custom request_validation_exception_handler was called")
    await log_api_error(
        request, req_body=str(exc.body), status_code=422, function_name=str(request.url)
    )
    return await _request_validation_exception_handler(request, exc)


async def http_exception_handler(
    request: Request, exc: HTTPException
) -> Union[JSONResponse, Response]:
    """
    This is a wrapper to the default HTTPException handler of FastAPI.
    This function will be called when a HTTPException is explicitly raised.
    """
    pydantic_basemodel = str(dict(getattr(request.state, "pydantic_basemodel", {})))
    logger.debug("Our custom http_exception_handler was called")
    await log_api_error(
        request,
        req_body=pydantic_basemodel,
        status_code=exc.status_code,
        function_name=str(request.url),
    )
    return await _http_exception_handler(request, exc)


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.debug("Our custom unhandled_exception_handler was called")
    host = getattr(getattr(request, "client", None), "host", None)
    port = getattr(getattr(request, "client", None), "port", None)
    url = (
        f"{request.url.path}?{request.query_params}"
        if request.query_params
        else request.url.path
    )
    exception_type, exception_value, exception_traceback = sys.exc_info()
    exception_name = getattr(exception_type, "__name__", None)
    error_details = f'{host}:{port} - "{request.method} {url}" 500 Internal Server Error <{exception_name}: {exception_value}>'
    logger.error(error_details)
    pydantic_basemodel = str(dict(getattr(request.state, "pydantic_basemodel", {})))

    # Ensure the following line is awaited in an asynchronous context
    await log_api_error(
        request, req_body=pydantic_basemodel, status_code=500, function_name=str(url)
    )
    return JSONResponse({"detail": str(exc)}, status_code=500)
