from __future__ import annotations

from typing import Any

from distributed_websocket import WebSocketManager as WebSocketManagerOriginal

from enums import EventType
from schemas import ApplicationResponse, Game


class WebSocketManager(WebSocketManagerOriginal):
    async def send_broadcast(self, game: Game, response: ApplicationResponse[Any]) -> None:
        players = {player.connection_id for player in game.players}
        for connection in self.active_connections:
            if connection.id in players:
                await connection.send_json(data=response.model_dump())

    async def send_error(self, connection_id: str, event_type: EventType) -> None:
        for connection in self.active_connections:
            if connection.id == connection_id:
                await connection.send_json(
                    data=ApplicationResponse[bool](
                        ok=False, result=False, event_type=event_type
                    ).model_dump()
                )

    async def send_message(self, connection_id: str, response: ApplicationResponse[Any]) -> None:
        for connection in self.active_connections:
            if connection.id == connection_id:
                await connection.send_json(data=response.model_dump())
