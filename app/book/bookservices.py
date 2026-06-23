from sqlmodel.ext.asyncio.session import AsyncSession
from schemas.bookschema import BookModel, UpdateBookModel
from sqlmodel import select, desc
from models.book import Book
from datetime import datetime
import uuid


class BookServices:
    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.execute(statement)
        return result.scalars().all()

    # get a single book details
    async def get_book(self, book_uid: uuid.UUID, session: AsyncSession):
        statement = select(Book).where(book_uid == Book.id)
        result = await session.execute(statement)
        return result.scalars().first()

    async def create_book(self, book: BookModel, session: AsyncSession):
        book_details = book.model_dump()
        new_book = Book(**book_details)
        session.add(new_book)
        await session.commit()
        return new_book

    async def update_book(
        self, book_uid: uuid.UUID, updated_book: UpdateBookModel, session: AsyncSession
    ):
        curr_book_details = await self.get_book(book_uid, session)
        if curr_book_details is not None:
            updated_book_details = updated_book.model_dump(exclude_unset=True)
            curr_book_details.updated_at = datetime.now()
            for key, value in updated_book_details.items():
                setattr(curr_book_details, key, value)
            await session.commit()
            return curr_book_details
        return None

    async def delete_book(self, book_uid: uuid.UUID, session: AsyncSession):
        book_to_delete = await self.get_book(book_uid, session)
        if book_to_delete is not None:
            await session.delete(book_to_delete)
            await session.commit()
            return "deleted successfully"
        return None
