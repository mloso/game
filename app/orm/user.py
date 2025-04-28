from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column

from .core import ORMModel, types


class UserModel(ORMModel):
    username: Mapped[types.String32] = mapped_column(unique=True, index=True)
    password: Mapped[types.String64]
