from __future__ import annotations

from typing import Optional, Type, Union

from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette import status

from exc import ApplicationError
from logger import logger


def add_exception_handler(
    application: FastAPI,
    exception_class_or_status_code: Union[Type[BaseException], int],
    error: Optional[str] = None,
) -> None:
    def default_exception_handler(
        request: Request,  # noqa
        exception: Exception,
    ) -> JSONResponse:
        if hasattr(default_exception_handler, "__error__"):
            error_ = default_exception_handler.__error__
        elif hasattr(exception, "detail"):
            error_ = exception.detail
        else:
            error_ = "UNKNOWN_ERROR"

        if hasattr(default_exception_handler, "__status_code__"):
            status_code = default_exception_handler.__status_code__
        else:
            if isinstance(exception, ApplicationError):
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            elif isinstance(exception, HTTPException):
                status_code = exception.status_code
            elif isinstance(exception, RequestValidationError):
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            elif isinstance(exception, ValidationError):
                status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            else:
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        logger.debug(
            "Error: status code(%s): %s: %s" % (status_code, type(exception), str(exception))
        )

        return JSONResponse(
            status_code=status_code,
            content={
                "ok": False,
                "error": error_,
                "error_code": status_code,
            },
        )

    function = default_exception_handler
    if isinstance(exception_class_or_status_code, int):
        function.__status_code__ = exception_class_or_status_code
    if error:
        function.__error__ = error

    application.add_exception_handler(exception_class_or_status_code, function)


def create_exception_handlers(application: FastAPI) -> None:
    add_exception_handler(application=application, exception_class_or_status_code=ApplicationError)
    add_exception_handler(application=application, exception_class_or_status_code=HTTPException)
    add_exception_handler(
        application=application,
        exception_class_or_status_code=RequestValidationError,
        error="REQUEST_VALIDATION_FAILED",
    )
    add_exception_handler(
        application=application,
        exception_class_or_status_code=ValidationError,
        error="REQUEST_VALIDATION_FAILED",
    )
