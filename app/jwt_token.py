from __future__ import annotations

from typing import Any

import jwt

from core.settings import jwt_settings


def decode_token(token: str) -> Any:
    return jwt.decode(
        jwt=token,
        key=jwt_settings.SECRET_KEY,
        algorithms=[jwt_settings.ALGORITHM],
    ).get("sub")


def encode_token(data: dict[str, Any]) -> str:
    return jwt.encode(payload=data, key=jwt_settings.SECRET_KEY, algorithm=jwt_settings.ALGORITHM)
