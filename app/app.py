from __future__ import annotations

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from redis.asyncio import Redis

from api import router as api_router
from core.exception_handlers import create_exception_handlers
from core.lifespan import lifespan
from core.middleware import create_middleware
from core.routes import create_routes
from core.settings import redis_settings, server_settings
from redis_accessor import RedisAccessor
from websocket_manager import WebSocketManager


def create_application() -> FastAPI:
    """
    Setup FastAPI application: middleware, exception handlers, logger.
    """

    docs_url, redoc_url, openapi_url, swagger_ui_oauth2_redirect_url = (
        "/docs",
        "/redoc",
        "/openapi.json",
        "/docs/oauth2-redirect",
    )
    if not server_settings.DEBUG:
        docs_url, redoc_url, openapi_url, swagger_ui_oauth2_redirect_url = (
            None,
            None,
            None,
            None,
        )

    application = FastAPI(
        title="game",
        description="Backend for playing game via websockets.",
        version="1.0",
        debug=server_settings.DEBUG,
        docs_url=docs_url,
        redoc_url=redoc_url,
        openapi_url=openapi_url,
        swagger_ui_oauth2_redirect_url=swagger_ui_oauth2_redirect_url,
        lifespan=lifespan,
    )
    application.include_router(api_router, tags=["API"])
    application.state.redis = Redis(
        host=redis_settings.REDIS_HOSTNAME, port=redis_settings.REDIS_PORT
    )
    application.state.redis_accessor = RedisAccessor(redis=application.state.redis)
    application.state.manager = WebSocketManager(
        broker_channel=redis_settings.REDIS_CHANNEL, broker_url=redis_settings.url
    )
    application.state.scheduler = AsyncIOScheduler()

    create_exception_handlers(application=application)
    create_middleware(application=application)
    create_routes(application=application)

    return application


app = create_application()
