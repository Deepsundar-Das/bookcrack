from fastapi import FastAPI
from db.db_config import fetch_all_books_direct
from contextlib import asynccontextmanager
from apis.authrouter import auth_route

@asynccontextmanager
async def life_span(app: FastAPI):
    await fetch_all_books_direct()
    yield


app = FastAPI(lifespan=life_span)
app.include_router(auth_route, prefix="/api/v1/auth")
