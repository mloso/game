from __future__ import annotations

import asyncio

from enums import EventType
from game_manager import GameManager
from metadata import GAME_START_TIME
from redis_accessor import RedisAccessor
from schemas import ApplicationResponse, Game
from websocket_manager import WebSocketManager


async def start_game_task(
    manager: WebSocketManager, game_id: str, redis_accessor: RedisAccessor
) -> None:
    await asyncio.sleep(GAME_START_TIME)

    game_manager = GameManager(game_id=game_id, redis_accessor=redis_accessor)
    if await game_manager.start():
        async with redis_accessor.access(game_id, model=Game) as data:
            await manager.send_broadcast(
                game=data[game_id],
                response=ApplicationResponse[bool](
                    ok=True, result=True, detail="STARTED", event_type=EventType.INFORMATION
                ),
            )
