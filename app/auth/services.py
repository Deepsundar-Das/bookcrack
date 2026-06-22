from schemas.userschema import CreateUser
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from .utils import get_hashed_password

class AuthServices:
    async def create_user(self, user: CreateUser, session: AsyncSession):
        user_data:dict = user.model_dump()
        hased_password: str = await get_hashed_password(user_data.get("password"))
        user_data['password'] = hased_password
        new_user: User = User(**user_data)
        session.add(new_user)
        await session.commit()
        return new_user
