from __future__ import annotations

from typing import Any

from fastapi import FastAPI, status

from schemas import ApplicationResponse


def create_healthcheck(application: FastAPI) -> None:
    @application.post(
        path="/",
        response_model=ApplicationResponse[bool],
        status_code=status.HTTP_200_OK,
    )
    async def healthcheck() -> dict[str, Any]:
        return {
            "ok": True,
            "result": True,
        }


def create_routes(application: FastAPI) -> None:
    create_healthcheck(application=application)
