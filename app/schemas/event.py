from __future__ import annotations

from typing import Any

from enums import EventType

from .schema import ApplicationSchema


class Event(ApplicationSchema):
    payload: dict[str, Any] | None = None
    event_type: EventType
