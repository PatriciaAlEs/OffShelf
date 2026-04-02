from __future__ import annotations

import requests
from flask import Blueprint, jsonify, request

from services.book_service import save_book
from services.google_books import transform_google_book_item

books_bp = Blueprint("books", __name__, url_prefix="/books")


@books_bp.get("/search")
def search_books():
    query = (request.args.get("q") or "").strip()
    if not query:
        return jsonify({"error": 'Missing required query parameter "q".'}), 400

    url = "https://www.googleapis.com/books/v1/volumes"
    try:
        response = requests.get(url, params={"q": query, "maxResults": 20}, timeout=5)
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
