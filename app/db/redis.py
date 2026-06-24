import redis.asyncio as aioredis
from appconfig import appConfig

REDIS_TOKEN_EXPIRY_TIME = 300

revoked_token_bucket = aioredis.Redis(
    host=appConfig.REDIS_HOST, port=appConfig.REDIS_PORT
)


async def add_revoked_token(sid: str):
    await revoked_token_bucket.set(
        name=sid, value="revoked", ex=REDIS_TOKEN_EXPIRY_TIME
    )
    print(f"added sid is {sid}")


async def is_sid_in_bucket(sid: str):
    print(f"I need to check if the sid {sid} is in bucket or not")
    res = await revoked_token_bucket.get(sid) is not None
    print(res)
    return res
