from passlib.context import CryptContext


cryptoContext = CryptContext(schemes=["bcrypt"])

async def get_hashed_password(password: str) -> str:
    return cryptoContext.hash(password)


async def verify_password(password: str, hashed_password: str) -> bool:
    return cryptoContext.verify(password, hashed_password)
