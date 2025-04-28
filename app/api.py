from __future__ import annotations

import datetime
from typing import Any

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from distributed_websocket import Connection
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Body, Depends
from fastapi.websockets import WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from authorization import authenticate_user
from core.depends import (
    get_redis_accessor,
    get_scheduler,
    get_session,
    get_user,
    get_websocket_manager,
)
from enums import EventType
from game_manager import GameManager
from jwt_token import encode_token
from logger import logger
from metadata import GAME_FIELD_SIZE, MAX_PLAYERS, PALETTE
from orm import GameStatModel, UserModel
from orm.core import async_sessionmaker
from password import hash_password
from redis_accessor import RedisAccessor
from schemas import ApplicationResponse, Event, Field, Game, Player
from tasks import start_game_task
from utils.id import generate_id
from websocket_manager import WebSocketManager

router = APIRouter()


@router.websocket(path="/{token}")
async def websocket_main_handler(
    websocket: WebSocket,
    user: UserModel = Depends(get_user),
    scheduler: AsyncIOScheduler = Depends(get_scheduler),
    manager: WebSocketManager = Depends(get_websocket_manager),
    redis_accessor: RedisAccessor = Depends(get_redis_accessor),
) -> None:
    connection = await manager.new_connection(websocket=websocket, conn_id=user.username)
    try:
        await websocket_handler(
            connection=connection,
            scheduler=scheduler,
            manager=manager,
            user=user,
            redis_accessor=redis_accessor,
        )
    except Exception:  # noqa
        manager.remove_connection(connection)


async def websocket_handler(
    connection: Connection,
    scheduler: AsyncIOScheduler,
    manager: WebSocketManager,
    user: UserModel,
    redis_accessor: RedisAccessor,
) -> None:
    while True:
        event = Event.model_validate(await connection.receive_json())
        try:
            await parse_event(
                connection=connection,
                scheduler=scheduler,
                manager=manager,
                event=event,
                user=user,
                redis_accessor=redis_accessor,
            )
        except WebSocketDisconnect:
            raise
        except (Exception, ValueError) as exc:
            logger.exception(exc)
            await manager.send_message(
                connection_id=connection.id,
                response=ApplicationResponse[bool](
                    ok=False, result=False, event_type=event.event_type
                ),
            )


async def parse_event(
    connection: Connection,
    scheduler: AsyncIOScheduler,
    manager: WebSocketManager,
    event: Event,
    user: UserModel,
    redis_accessor: RedisAccessor,
) -> None:
    match event.event_type:
        case EventType.CREATE:
            await create_handler(
                connection=connection, manager=manager, redis_accessor=redis_accessor
            )
        case EventType.EXIT:
            await exit_handler(
                connection=connection, manager=manager, redis_accessor=redis_accessor
            )
        case EventType.GET_ME:
            await get_me_handler(
                connection=connection, manager=manager, redis_accessor=redis_accessor
            )
        case EventType.JOIN:
            await join_handler(
                connection=connection,
                manager=manager,
                event=event,
                user=user,
                redis_accessor=redis_accessor,
            )
        case EventType.INFORMATION:
            await information_handler(
                connection=connection, manager=manager, redis_accessor=redis_accessor
            )
        case EventType.MOVE:
            await move_handler(
                connection=connection, manager=manager, event=event, redis_accessor=redis_accessor
            )
        case EventType.SELECT_COLOR:
            await select_color_handler(
                connection=connection,
                manager=manager,
                scheduler=scheduler,
                event=event,
                redis_accessor=redis_accessor,
            )
        case EventType.STATS:
            await stats_handler(connection=connection, manager=manager, user=user)


async def create_handler(
    connection: Connection,
    manager: WebSocketManager,
    redis_accessor: RedisAccessor,
) -> None:
    game_id = f"game_{generate_id()}"
    async with redis_accessor.access(game_id, model=Game) as data:
        data[game_id] = Game(
            id=game_id,
            field=[
                [Field(x=x, y=y) for x in range(GAME_FIELD_SIZE)] for y in range(GAME_FIELD_SIZE)
            ],
            colors=list(PALETTE),
        )

    await manager.send_message(
        connection_id=connection.id,
        response=ApplicationResponse[str](ok=True, result=game_id, event_type=EventType.CREATE),
    )


async def exit_handler(
    connection: Connection, manager: WebSocketManager, redis_accessor: RedisAccessor
) -> None:
    async with redis_accessor.access(connection.id, model=Player) as data:
        if data[connection.id] is None:
            return await manager.send_error(connection_id=connection.id, event_type=EventType.EXIT)

        game_manager = GameManager(
            game_id=data[connection.id].game_id, redis_accessor=redis_accessor
        )
        if not await game_manager.remove_player(connection_id=connection.id):
            return await manager.send_error(connection_id=connection.id, event_type=EventType.EXIT)

        data[connection.id] = None

    await manager.send_message(
        connection_id=connection.id,
        response=ApplicationResponse[bool](ok=True, result=True, event_type=EventType.EXIT),
    )


async def get_me_handler(
    connection: Connection, manager: WebSocketManager, redis_accessor: RedisAccessor
) -> None:
    try:
        async with redis_accessor.access(connection.id, model=Player) as data:
            async with async_sessionmaker.begin() as session:
                user = await UserModel.get_by(session, username=data[connection.id].username)
    except Exception:  # noqa
        return await manager.send_error(connection_id=connection.id, event_type=EventType.GET_ME)

    await manager.send_message(
        connection_id=connection.id,
        response=ApplicationResponse[dict[str, Any]](
            ok=True, result={"username": user.username}, event_type=EventType.GET_ME
        ),
    )


async def join_handler(
    connection: Connection,
    manager: WebSocketManager,
    event: Event,
    user: UserModel,
    redis_accessor: RedisAccessor,
) -> None:
    async with redis_accessor.access(connection.id, model=Player) as data:
        if not event.payload.get("game_id", None):
            return await manager.send_error(connection_id=connection.id, event_type=EventType.JOIN)

        data[connection.id] = Player(
            connection_id=connection.id, username=user.username, game_id=event.payload["game_id"]
        )
        game_manager = GameManager(game_id=event.payload["game_id"], redis_accessor=redis_accessor)

        if not await game_manager.add_player(new_player=data[connection.id]):
            data[connection.id] = None

            return await manager.send_error(connection_id=connection.id, event_type=EventType.JOIN)

        async with redis_accessor.access(game_manager.game_id, model=Game) as game_data:
            await manager.send_broadcast(
                game=game_data[game_manager.game_id],
                response=ApplicationResponse[Game](
                    ok=True,
                    result=game_data[game_manager.game_id],
                    detail="INFORMATION",
                    event_type=EventType.INFORMATION,
                ),
            )

    await manager.send_message(
        connection_id=connection.id,
        response=ApplicationResponse[bool](ok=True, result=True, event_type=EventType.JOIN),
    )


async def information_handler(
    connection: Connection, manager: WebSocketManager, redis_accessor: RedisAccessor
) -> None:
    async with redis_accessor.access(connection.id, model=Player) as data:
        if data[connection.id] is None:
            return await manager.send_error(
                connection_id=connection.id, event_type=EventType.INFORMATION
            )

        async with redis_accessor.access(data[connection.id].game_id, model=Game) as game_data:
            await manager.send_message(
                connection_id=connection.id,
                response=ApplicationResponse[Game](
                    ok=True,
                    result=game_data[data[connection.id].game_id],
                    event_type=EventType.INFORMATION,
                    detail="INFORMATION",
                ),
            )


async def move_handler(
    connection: Connection, manager: WebSocketManager, event: Event, redis_accessor: RedisAccessor
) -> None:
    async with redis_accessor.access(connection.id, model=Player) as data:
        game_manager = GameManager(
            game_id=data[connection.id].game_id, redis_accessor=redis_accessor
        )

    move = await game_manager.make_move(
        connection_id=connection.id, x=int(event.payload["x"]), y=int(event.payload["y"])
    )
    if isinstance(move, bool):
        if not move:
            await manager.send_error(connection_id=connection.id, event_type=EventType.MOVE)
        else:
            async with redis_accessor.access(game_manager.game_id, model=Game) as game_data:
                await manager.send_broadcast(
                    game=game_data[game_manager.game_id],
                    response=ApplicationResponse[Game](
                        ok=True,
                        result=game_data[game_manager.game_id],
                        event_type=EventType.INFORMATION,
                        detail="INFORMATION",
                    ),
                )
    else:
        async with redis_accessor.access(game_manager.game_id, model=Game) as game_data:
            async with async_sessionmaker.begin() as session:
                for player in game_data[game_manager.game_id].players:
                    await GameStatModel.create(
                        session,
                        values={
                            GameStatModel.is_won: player.username
                            in {winner.username for winner in move},
                            GameStatModel.successfully_clicks: player.score,
                            GameStatModel.unsuccessfully_clicks: player.unsuccessfully_score,
                            GameStatModel.color: player.color,
                            GameStatModel.user_id: (
                                await UserModel.get_by(session, username=player.username)
                            ).id,
                        },
                    )

            async with redis_accessor.access(
                *[player.connection_id for player in game_data[game_manager.game_id].players],
                model=Player,
            ) as data:
                for player in game_data[game_manager.game_id].players:
                    data[player.connection_id] = None

            await manager.send_broadcast(
                game=game_data[game_manager.game_id],
                response=ApplicationResponse[Game](
                    ok=True,
                    result=game_data[game_manager.game_id],
                    event_type=EventType.INFORMATION,
                    detail="INFORMATION",
                ),
            )
            await manager.send_broadcast(
                game=game_data[game_manager.game_id],
                response=ApplicationResponse[list[Player]](
                    ok=True, result=move, event_type=EventType.INFORMATION, detail="WINNERS"
                ),
            )
            game_data[game_manager.game_id] = None


async def select_color_handler(
    connection: Connection,
    manager: WebSocketManager,
    scheduler: AsyncIOScheduler,
    event: Event,
    redis_accessor: RedisAccessor,
) -> None:
    async with redis_accessor.access(connection.id, model=Player) as data:
        game_manager = GameManager(
            game_id=data[connection.id].game_id, redis_accessor=redis_accessor
        )
        if not await game_manager.select_color(
            connection_id=connection.id, color=event.payload.get("color", None)
        ):
            return await manager.send_error(
                connection_id=connection.id, event_type=EventType.SELECT_COLOR
            )

        async with redis_accessor.access(game_manager.game_id, model=Game) as game_data:
            await manager.send_broadcast(
                game=game_data[game_manager.game_id],
                response=ApplicationResponse[Game](
                    ok=True,
                    result=game_data[game_manager.game_id],
                    event_type=EventType.INFORMATION,
                    detail="INFORMATION",
                ),
            )
            if len(game_data[game_manager.game_id].players) == MAX_PLAYERS and all(
                bool(player.color) for player in game_data[game_manager.game_id].players
            ):
                scheduler.add_job(
                    func=start_game_task,
                    kwargs={
                        "manager": manager,
                        "game_id": game_manager.game_id,
                        "redis_accessor": redis_accessor,
                    },
                    trigger="date",
                    max_instances=1,
                    run_date=datetime.datetime.now(),
                )

    await manager.send_message(
        connection_id=connection.id,
        response=ApplicationResponse[str](
            ok=True, result=event.payload["color"], event_type=EventType.SELECT_COLOR
        ),
    )


async def stats_handler(
    connection: Connection, manager: WebSocketManager, user: UserModel
) -> None:
    async with async_sessionmaker.begin() as session:
        await manager.send_message(
            connection_id=connection.id,
            response=ApplicationResponse[dict[str, Any]](
                ok=True,
                result=await GameStatModel.information(session, user_id=user.id),
                event_type=EventType.STATS,
            ),
        )


@router.post(
    path="/login",
    response_model=ApplicationResponse[dict[str, Any]],
    status_code=status.HTTP_200_OK,
)
async def login_handler(
    username: str = Body(...),
    password: str = Body(...),
    session: AsyncSession = Depends(get_session),
) -> dict[str, Any]:
    user = await authenticate_user(session=session, username=username, password=password)
    if not user:
        raise HTTPException(
            detail="FORBIDDEN",
            headers={"WWW-Authenticate": "Bearer"},
            status_code=status.HTTP_403_FORBIDDEN,
        )

    return {
        "ok": True,
        "result": {
            "token": encode_token(data={"sub": user.username}),
            "token_type": "bearer",
        },
    }


@router.post(
    path="/register",
    response_model=ApplicationResponse[dict[str, Any]],
    status_code=status.HTTP_200_OK,
)
async def register_handler(
    username: str = Body(min_length=3, max_length=32),
    password: str = Body(min_length=3, max_length=8),
    session: AsyncSession = Depends(get_session),
) -> dict[str, Any]:
    if await UserModel.get_by(session, username=username):
        raise HTTPException(detail="NOT_FOUND", status_code=status.HTTP_404_NOT_FOUND)

    user = await UserModel.create(
        session,
        values={
            UserModel.username: username,
            UserModel.password: hash_password(plain_password=password),
        },
    )

    return {
        "ok": True,
        "result": {
            "token": encode_token(data={"sub": user.username}),
            "token_type": "bearer",
        },
    }
