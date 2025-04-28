from __future__ import annotations

from typing import Annotated, Final

from sqlalchemy import ForeignKey, types
from sqlalchemy.orm import mapped_column

Int: type[int] = Annotated[int, mapped_column(types.INT)]
BigInt: type[int] = Annotated[int, mapped_column(types.BIGINT)]

String32: type[str] = Annotated[str, mapped_column(types.String(32))]
String64: type[str] = Annotated[str, mapped_column(types.String(64))]

USER_TABLE_NAME: Final[str] = "users"
UserID: type[int] = Annotated[int, mapped_column(ForeignKey(f"{USER_TABLE_NAME}.id"))]
