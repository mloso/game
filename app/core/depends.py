from __future__ import annotations

from distributed_websocket import WebSocketManager
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends, Path
from fastapi.websockets import WebSocket
from jwt import InvalidTokenError
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from jwt_token import decode_token
from orm import UserModel
from orm.core import async_sessionmaker


async def get_session() -> AsyncSession:  # type: ignore[misc]
    async with async_sessionmaker.begin() as session:
        yield session


async def get_user(
    session: AsyncSession = Depends(get_session), token: str = Path(...)
) -> UserModel:
    try:
        username = decode_token(token=token)
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT_FOUND")
    if username is None or (user := await UserModel.get_by(session, username=username)) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT_FOUND")

    return user


def get_redis_accessor(websocket: WebSocket) -> Redis:
    return websocket.app.state.redis_accessor


def get_scheduler(websocket: WebSocket) -> Redis:
    return websocket.app.state.scheduler


def get_websocket_manager(websocket: WebSocket) -> WebSocketManager:
    return websocket.app.state.manager
