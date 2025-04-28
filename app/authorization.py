from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from orm import UserModel
from password import verify_password


async def authenticate_user(
    session: AsyncSession, username: str, password: str
) -> bool | UserModel:
    user = await UserModel.get_by(session, username=username)
    if not user:
        return False
    if not verify_password(plain_password=password, hashed_password=user.password):
        return False

    return user
