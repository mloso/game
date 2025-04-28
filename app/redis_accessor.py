from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Generic, TypeVar

from pydantic import BaseModel
from redis.asyncio import Redis

T = TypeVar("T", bound=BaseModel)


class RedisAccessor:
    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    @asynccontextmanager
    async def access(self, *keys: str, model: type[T]) -> RedisAccessorContext[T]:
        context = RedisAccessorContext[T](self, keys=keys, model=model)
        await context.load_values()

        try:
            yield context
        finally:
            await self.commit_updates(updates=context.updates)

    async def commit_updates(self, updates: dict[str, T | None]) -> None:
        if updates:
            async with self.redis.pipeline(transaction=True) as pipe:
                for key, value in updates.items():
                    if value is None:
                        await pipe.delete(key)
                    else:
                        await pipe.set(key, value.model_dump_json())
                await pipe.execute()

    async def get(self, key: str, model: type[T]) -> T | None:
        value = await self.redis.get(name=key)
        if not value:
            return None

        try:
            return model.model_validate_json(value)
        except ValueError as exc:
            raise ValueError(f"Failed to deserialize Redis value for key {key}") from exc


class RedisAccessorContext(Generic[T]):
    def __init__(self, accessor: RedisAccessor, keys: tuple[str], model: type[T]) -> None:
        self.accessor = accessor
        self.keys = keys
        self.model = model

        self.updates: dict[str, T | None] = {}
        self.values: dict[str, T | None] = {}

    async def load_values(self):
        for key in self.keys:
            self.values[key] = await self.accessor.get(key, model=self.model)

    def __getitem__(self, key: str) -> T | None:
        if key not in self.keys:
            raise KeyError(f"Key {key} was not requested in context")

        return self.values[key]

    def __setitem__(self, key: str, value: T | None) -> None:
        if key not in self.keys:
            raise KeyError(f"Key {key} was not requested in context")

        if self.model and value is not None and not isinstance(value, self.model):
            raise ValueError(f"Value must be instance of {self.model.__name__}")

        self.values[key] = value
        self.updates[key] = value
