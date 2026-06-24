from passlib.context import CryptContext
from appconfig import appConfig
import jwt
from datetime import timedelta, datetime, timezone
import uuid
import logging
import bcrypt

# -------------------------------------------PASSWORD HASHING AND VERIFICATION----------------------------------------


async def get_hashed_password(password: str) -> str:
    # Convert string to bytes
    password_bytes = password.encode("utf-8")
    # Generate salt and hash
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    # Return as a string to save in the DB
    return hashed_bytes.decode("utf-8")


async def verify_password(password: str, hashed_password: str) -> bool:
    password_bytes = password.encode("utf-8")
    hash_bytes = hashed_password.encode("utf-8")
    # Let bcrypt compare them safely
    return bcrypt.checkpw(password_bytes, hash_bytes)


# --------------------------------------------------------JWT--------------------------------------------------------

JWT_ALGORITHM = appConfig.JWT_ALGORITHM
JWT_SECRET = appConfig.JWT_SECRET
JWT_ACCESS_EXPIRY_TIME = timedelta(seconds=300)
JWT_REFRESH_EXPIRY_TIME = timedelta(seconds=600)


async def get_jwt_token(
    user: dict, sid: str, expiry_time: timedelta = JWT_ACCESS_EXPIRY_TIME, refresh: bool = False
):
    payload = {}
    payload["user"] = user
    payload["exp_time"] = str(datetime.now(timezone.utc) + expiry_time)
    payload["refresh"] = refresh
    payload["jti"] = str(uuid.uuid4())
    payload["sid"] = sid
    encdoded_jwt = jwt.encode(
        payload=payload,
        key=JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )
    print(f"jti is {payload['jti']}")
    return encdoded_jwt


async def decode_jwt_token(token: str):
    try:
        decoded_jwt = jwt.decode(jwt=token, algorithms=[JWT_ALGORITHM], key=JWT_SECRET)
        return decoded_jwt
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None
