from __future__ import annotations

from .schema import ApplicationSchema


class Player(ApplicationSchema):
    connection_id: str
    username: str
    game_id: str
    color: str | None = None
    score: int = 0
    unsuccessfully_score: int = 0
