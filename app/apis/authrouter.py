from fastapi import APIRouter, Depends
from schemas.userschema import CreateUser
from auth.services import AuthServices
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_config import get_session

auth_route = APIRouter()
auth_service = AuthServices()

@auth_route.post('/signup')
async def user_signup(user: CreateUser, session: AsyncSession = Depends(get_session)):
    return await auth_service.create_user(user, session)
