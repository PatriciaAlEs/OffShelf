from __future__ import annotations

import requests
from flask import Blueprint, jsonify, request
from sqlalchemy import func

from models import Book
from services.book_service import save_book
from services.google_books import transform_google_book_item

books_bp = Blueprint("books", __name__, url_prefix="/books")


def _parse_bool_param(value: str) -> bool | None:
    lowered = value.strip().lower()
    if lowered in ("true", "1", "yes"):
        return True
    if lowered in ("false", "0", "no"):
        return False
    return None


@books_bp.get("")
def list_books():
    query = Book.query

    language = (request.args.get("language") or "").strip()
    if language:
        query = query.filter(func.lower(Book.language) == language.lower())

    is_indie_raw = request.args.get("is_indie")
    if is_indie_raw is not None and is_indie_raw != "":
        parsed = _parse_bool_param(is_indie_raw)
        if parsed is None:
            return (
                jsonify(
                    {
                        "error": 'Invalid "is_indie" value; use true or false.',
                    }
                ),
                400,
            )
        query = query.filter(Book.is_indie == parsed)

    books = query.order_by(Book.created_at.desc()).all()
    return jsonify([book.to_dict() for book in books]), 200


@books_bp.get("/search")
def search_books():
    query = (request.args.get("q") or "").strip()
    if not query:
        return jsonify({"error": 'Missing required query parameter "q".'}), 400

    limit = request.args.get("limit", default=20, type=int)
    # seguridad (MUY importante)
    limit = min(limit, 50)

    url = "https://www.googleapis.com/books/v1/volumes"
    try:
        response = requests.get(url, params={"q": query, "maxResults": limit}, timeout=5)
        response.raise_for_status()
        payload = response.json()
    except Exception:
        return jsonify({"error": "Failed to fetch books"}), 500

    items = payload.get("items", [])
    if not items:
        return jsonify([]), 200

    saved_books = []
    for item in items:
        book_data = transform_google_book_item(item)
        if not book_data.get("title"):
            continue
        book = save_book(book_data)
        saved_books.append(book.to_dict())

    print(f"Fetched {len(items)} books, saved {len(saved_books)}")
    return jsonify(saved_books), 200
