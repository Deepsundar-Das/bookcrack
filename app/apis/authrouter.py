from fastapi import APIRouter, Depends, status, HTTPException
from schemas.userschema import CreateUser, LoginUser
from auth.services import AuthServices
from auth.utils import get_jwt_access_token, verify_password
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_config import get_session
from datetime import timedelta
from fastapi.responses import JSONResponse

auth_route = APIRouter()
auth_service = AuthServices()


@auth_route.post("/signup")
async def user_signup(user: CreateUser, session: AsyncSession = Depends(get_session)):
    return await auth_service.create_user(user, session)


@auth_route.post("/login")
async def user_login(user: LoginUser, session: AsyncSession = Depends(get_session)):
    user_email = user.email
    user_password = user.password
    user_details = await auth_service.get_uer_by_email(user_email, session=session)
    if user_details is not None:
        uid = str(user_details.id)
        if await verify_password(user_password, user_details.password):
            access_token = await get_jwt_access_token(
                user={"email": user_email, "uid": uid}
            )
            refresh_token = await get_jwt_access_token(
                user={"email": user_email, "uid": uid},
                refresh=True,
                expiry_time=timedelta(seconds=720),
            )

            return JSONResponse(
                content={
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user email": user_email,
                    "user uid": uid,
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="wrong password"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="wrong email"
        )
