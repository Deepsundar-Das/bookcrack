from fastapi import APIRouter, Depends, status, HTTPException
from schemas.userschema import CreateUser, LoginUser
from auth.services import AuthServices
from auth.utils import get_jwt_token, verify_password, decode_jwt_token
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_config import get_session
from datetime import timedelta
from fastapi.responses import JSONResponse
from auth.dependencies import RefreshTokenBearer
from auth.dependencies import AccessTokenBearer
from db.redis import add_revoked_token
import uuid

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

            sid: str = str(uuid.uuid4())

            refresh_token = await get_jwt_token(
                user={"email": user_email, "uid": uid},
                sid=sid
            )

            access_token = await get_jwt_token(
                user={"email": user_email, "uid": uid},
                sid=sid
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


@auth_route.post("/getaccesstoken")
async def get_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    print(token_details.get("user"))
    print(token_details.get("jti"))
    return JSONResponse(
        content={"token": await get_jwt_token(user=token_details.get("user"), sid=token_details.get("sid"))}
    )


@auth_route.post("/logout")
# 1. add AccessToken to redis
# 2. add refresh token to postgres
async def logout(token_data: dict = Depends(AccessTokenBearer())):
    await add_revoked_token(token_data.get("sid"))
    return JSONResponse(
        content={"message": "Logged out successfully"}, status_code=status.HTTP_200_OK
    )
