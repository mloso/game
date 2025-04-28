from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict

from enums import EventType

GameType = TypeVar("GameType", bound=Any)


class _BaseModel(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        from_attributes=True,
    )


class ApplicationSchema(_BaseModel): ...


class ApplicationResponse(_BaseModel, Generic[GameType]):
    ok: bool
    result: GameType | None = None
    event_type: EventType | None = None
    detail: str | None = None
    error: str | None = None
    error_code: int | None = None
