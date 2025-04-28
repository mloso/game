from __future__ import annotations

from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped

from .core import ORMModel, types


class GameStatModel(ORMModel):
    is_won: Mapped[bool]
    unsuccessfully_clicks: Mapped[types.Int]
    successfully_clicks: Mapped[types.Int]
    color: Mapped[types.String32]

    user_id: Mapped[types.UserID]

    @hybrid_property
    def total_clicks(self) -> int:
        return self.unsuccessfully_clicks + self.successfully_clicks

    @classmethod
    async def information(cls, session: AsyncSession, /, user_id: int) -> Any:
        statement = select(
            func.count().label("total_games"),
            func.sum(cls.successfully_clicks).label("successfully_clicks"),
            func.sum(cls.unsuccessfully_clicks).label("unsuccessfully_clicks"),
            select(
                select(cls.color, func.count().label("count"))
                .where(cls.user_id == user_id)
                .group_by(cls.color)
                .order_by(func.count().desc())
                .limit(1)
                .subquery()
                .c.color
            )
            .scalar_subquery()
            .label("most_used_color"),
        ).where(cls.user_id == user_id)
        return cls._one_row(result=cls._mappings(result=await session.execute(statement)))
