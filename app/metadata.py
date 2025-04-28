from __future__ import annotations

from typing import Final

GAME_START_TIME: Final[int] = 15

GAME_FIELD_SIZE: Final[int] = 10

URANDOM_SIZE: Final[int] = 8
"""Using in function: `os.random` as `__size` argument."""

MAX_PLAYERS: Final[int] = 4

PALETTE: Final[set[str]] = {
    "red",
    "orange",
    "yellow",
    "lime",
    "green",
    "teal",
    "cyan",
    "blue",
    "darkblue",
    "purple",
    "magenta",
    "pink",
    "gold",
    "silver",
    "gray",
    "black",
}

POOL_RECYCLE: Final[int] = 60 * 5
"""Value for recycle pool: 300 seconds."""
