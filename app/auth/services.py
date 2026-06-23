from schemas.userschema import CreateUser, LoginUser
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.user import User
from .utils import get_hashed_password, verify_password
from pydantic import EmailStr


class AuthServices:

    async def get_uer_by_email(
        self, email: EmailStr, session: AsyncSession
    ) -> User | None:
        statement = select(User).where(email == User.email)
        result = await session.execute(statement=statement)
        return result.scalar_one_or_none()

    async def does_user_exist(
        self, email: EmailStr, session: AsyncSession
    ) -> User | None:
        return await self.get_uer_by_email(email, session)

    async def create_user(self, user: CreateUser, session: AsyncSession) -> User:
        user_data: dict = user.model_dump()
        hased_password: str = await get_hashed_password(user_data.get("password"))
        user_data["password"] = hased_password
        new_user: User = User(**user_data)
        session.add(new_user)
        await session.commit()
        return new_user

    async def login_user(self, user: LoginUser, session: AsyncSession):
        user_data = await self.does_user_exist(user.email, session)
        if user_data is not None:
            return await verify_password(user.password, user_data.password)
        return None
