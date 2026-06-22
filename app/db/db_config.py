from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from appconfig import appConfig
from sqlmodel import text

db_engine = create_async_engine(url=appConfig.DATABASE_URL)

async_session_factory = async_sessionmaker(bind=db_engine, expire_on_commit=False, class_=AsyncSession)

async def get_session() -> AsyncSession:
    async with async_session_factory() as session:
        yield session


async def fetch_all_books_direct():
    async with db_engine.connect() as conn:
        sql_command = text("SELECT 'this is a test for database connection';")
        result = await conn.execute(sql_command)
        print(result.all())
