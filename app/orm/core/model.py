from __future__ import annotations

from typing import Any, Self, cast

import stringcase
from sqlalchemy import MappingResult, Result, ScalarResult, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, declared_attr, mapped_column
from sqlalchemy.orm.attributes import Mapped

from .types import BigInt


class ORMModel(DeclarativeBase):
    id: Mapped[BigInt] = mapped_column(unique=True, primary_key=True)

    @declared_attr  # type: ignore
    def __tablename__(cls) -> str:  # noqa
        return cast(str, stringcase.snakecase(cls.__name__.split("Model")[0]) + "s")

    @classmethod
    def _rows(cls, result: Result[Any]) -> ScalarResult[Any]:
        return result.scalars()

    @classmethod
    def _mappings(cls, result: Result[Any]) -> MappingResult[Any]:
        return result.mappings()

    @classmethod
    def _one_row(cls, result: Any) -> Self | None:
        return result.one_or_none()

    @classmethod
    def _where_for_all_attributes(
        cls,
        statement: Any,
        /,
        **kwargs: Any,
    ) -> Any:
        return statement.where(
            *[
                getattr(cls, __attr__) == kwargs.get(__attr__)
                for __attr__ in cls.__dict__
                if not __attr__.startswith("__")
                and not __attr__.endswith("__")
                and not __attr__.startswith("_")
                and kwargs.get(__attr__, None)
            ]
        )

    @classmethod
    async def create(cls, session: AsyncSession, /, values: dict[Any, Any]) -> Self:
        statement = insert(cls)
        return cls._one_row(
            result=cls._rows(result=await session.execute(statement.values(values).returning(cls)))
        )

    @classmethod
    async def get_by(cls, session: AsyncSession, /, **kwargs: Any) -> Self:
        statement = select(cls)
        return cls._one_row(
            result=cls._rows(
                result=await session.execute(cls._where_for_all_attributes(statement, **kwargs))
            )
        )
