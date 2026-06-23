from fastapi import APIRouter, HTTPException, Depends
from schemas.bookschema import BookModel, UpdateBookModel
from book.bookservices import BookServices
from db.db_config import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from models.book import Book
import uuid
from auth.dependencies import AccessTokenBearer, RefreshTokenBearer
from datetime import datetime

bookrouter = APIRouter()
services = BookServices()
accessTokenBearer = AccessTokenBearer()
refreshTokenBearer = RefreshTokenBearer()


@bookrouter.get("/books", status_code=200)
async def get_books(
    session: AsyncSession = Depends(get_session),
    userDetails=Depends(refreshTokenBearer),
):
    return await services.get_all_books(session)


@bookrouter.post("/book", status_code=201, response_model=Book)
async def add_book(
    book: BookModel,
    session: AsyncSession = Depends(get_session),
    userDetails=Depends(accessTokenBearer),
):
    # there is no checking mechanism to check if the book already exists or not, it is only for practice only
    book = await services.create_book(book, session)
    if book:
        return book
    else:
        raise HTTPException(status_code=404, detail="book not found")


@bookrouter.patch("/updateBook/{bookId}", status_code=200)
async def update_book(
    bookId: uuid.UUID,
    updatedBook: UpdateBookModel,
    session: AsyncSession = Depends(get_session),
    userDetails=Depends(accessTokenBearer),
):
    book = await services.update_book(bookId, updatedBook, session)
    if book:
        return book
    else:
        raise HTTPException(status_code=404, detail="book not found")


@bookrouter.delete("/book/{bookId}", status_code=200)
async def delete_book(
    bookId: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    userDetails=Depends(accessTokenBearer),
):
    response = await services.delete_book(bookId, session)
    if response != None:
        return response
    else:
        raise HTTPException(status_code=404, detail="book not found")
