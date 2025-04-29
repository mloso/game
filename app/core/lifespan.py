from __future__ import annotations

import datetime
from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI

from logger import logger
from redis_accessor import RedisAccessor
from tasks import start_game_task
from websocket_manager import WebSocketManager


async def restart_tasks(
    manager: WebSocketManager, redis_accessor: RedisAccessor, scheduler: AsyncIOScheduler
) -> None:
    async for game_id in redis_accessor.redis.scan_iter(match="game_*"):
        scheduler.add_job(
            func=start_game_task,
            kwargs={
                "manager": manager,
                "game_id": game_id,
                "redis_accessor": redis_accessor,
            },
            trigger="date",
            max_instances=1,
            run_date=datetime.datetime.now(),
        )


@asynccontextmanager
async def lifespan(application: FastAPI) -> None:
    logger.info(f"Application startup. Debug mode - {application.debug}")
    logger.info("Starting scheduler")
    application.state.scheduler.start()
    await restart_tasks(
        manager=application.state.manager,
        redis_accessor=application.state.redis_accessor,
        scheduler=application.state.scheduler,
    )
    yield
    logger.info("Application shutdown.")
    logger.info("Shutting down scheduler")
    application.state.scheduler.shutdown()
    await application.state.redis.aclose()
