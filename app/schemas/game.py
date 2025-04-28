from __future__ import annotations

from pydantic import Field as PydanticField

from .field import Field
from .player import Player
from .schema import ApplicationSchema


class Game(ApplicationSchema):
    id: str
    players: list[Player] = PydanticField(default_factory=list)
    field: list[list[Field]] = PydanticField(default_factory=list)
    colors: list[str]
    is_started: bool = False
    is_over: bool = False
