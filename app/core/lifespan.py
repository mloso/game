from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from logger import logger


@asynccontextmanager
async def lifespan(application: FastAPI) -> None:
    logger.info(f"Application startup. Debug mode - {application.debug}")
    logger.info("Starting scheduler")
    application.state.scheduler.start()
    yield
    logger.info("Application shutdown.")
    logger.info("Shutting down scheduler")
    application.state.scheduler.shutdown()
    await application.state.redis.aclose()
