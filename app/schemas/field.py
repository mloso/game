from __future__ import annotations

from .player import Player
from .schema import ApplicationSchema


class Field(ApplicationSchema):
    x: int
    y: int
    player: Player | None = None
