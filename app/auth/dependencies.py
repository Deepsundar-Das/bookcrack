from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException, status
from .utils import decode_jwt_token
from datetime import datetime


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        creds = await super().__call__(request)
        cred_token = creds.credentials
        cred_data = await decode_jwt_token(cred_token)

        if cred_data is not None:
            return await self.verify_token_data(cred_data)

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid credential or expired credential, credential is : {cred_data}",
        )

    async def verify_token_data(self, token_data: dict):
        raise NotImplementedError("override the TokenBearer verify_token_data method")


class AccessTokenBearer(TokenBearer):
    async def verify_token_data(self, token_data: dict):
        # 1. check token type
        if token_data.get("refresh"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="not a valid access token, please provide a valid access token",
            )

        # 2. check expiry time
        elif datetime.fromisoformat(token_data.get("exp_time")) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="access token expired, generate a new access token",
            )
        return token_data


class RefreshTokenBearer(TokenBearer):
    # 1. check token type
    async def verify_token_data(self, token_data: dict):
        if not token_data.get("refresh"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="invalid refresh token, provide a valid refresh token",
            )

        # 2. check expiry time
        elif datetime.fromisoformat(token_data.get("exp_time")) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="refresh token is expired"
            )

        return token_data
