from __future__ import annotations

from enum import Enum


class EventType(str, Enum):
    CREATE = "create"
    EXIT = "exit"
    GET_ME = "get_me"
    JOIN = "join"
    INFORMATION = "information"
    MOVE = "move"
    SELECT_COLOR = "select_color"
    STATS = "stats"
