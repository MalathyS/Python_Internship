from logging_config import logger
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from exceptions import DuplicateEmployeeEmailError

logger = logging.getLogger(__name__)

def register_exception_handlers(app: FastAPI):

    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request,
        exc: Exception,
    ):
        logger.exception(
            "Unhandled error on %s %s",
            request.method,
            request.url.path,
        )
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )
    @app.exception_handler(DuplicateEmployeeEmailError)
    async def duplicate_email_handler(
        request: Request,
        exc: DuplicateEmployeeEmailError,
    ):
        return JSONResponse(
            status_code=409,
            content={"detail": "An employee with this email already exists"},
        )

