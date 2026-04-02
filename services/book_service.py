from __future__ import annotations

from typing import Any

from extensions import db
from models import Book


def save_book(book_data: dict[str, Any]) -> Book:
    """Save a book if needed, or return an existing one by ISBN."""
    isbn = book_data.get("isbn")
    if isbn:
        existing_book = Book.query.filter_by(isbn=isbn).first()
        if existing_book:
            return existing_book

    title = book_data.get("title")
    if not title:
        raise ValueError("title is required when creating a new book")

    book = Book(
        title=title,
        authors=book_data.get("authors") or [],
        description=book_data.get("description"),
        language=book_data.get("language"),
        isbn=isbn,
        thumbnail=book_data.get("thumbnail"),
        categories=book_data.get("categories") or [],
        is_indie=bool(book_data.get("is_indie", False)),
    )
    db.session.add(book)
    db.session.commit()
    return book
