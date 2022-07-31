from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models import User, create_async_session
from schemas import UserSchema, UserInDBSchema


class CRUDUser:

    @staticmethod
    @create_async_session
    async def add(user: UserSchema, session: AsyncSession = None) -> bool:
        user = User(
            **user.dict()
        )
        session.add(user)
        try:
            await session.commit()
        except IntegrityError:
            return False
        else:
            return True

    @staticmethod
    @create_async_session
    async def get(user_id: int, session: AsyncSession = None) -> UserInDBSchema | None:
        user = await session.execute(
            select(User).where(User.id == user_id)
        )
        user = user.first()
        if user:
            return UserInDBSchema(**user[0].__dict__)

    @staticmethod
    @create_async_session
    async def get_by_username(username: str, session: AsyncSession = None) -> UserInDBSchema | None:
        user = await session.execute(
            select(User).where(User.username == username)
        )
        user = user.first()
        if user:
            return UserInDBSchema(**user[0].__dict__)
