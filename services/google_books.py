from __future__ import annotations

from typing import Any


def _extract_isbn(industry_identifiers: list[dict[str, Any]]) -> str | None:
    """Return preferred ISBN (ISBN_13 first, then ISBN_10)."""
    isbn_10 = None
    for identifier in industry_identifiers:
        id_type = identifier.get("type")
        value = identifier.get("identifier")
        if not value:
            continue
        if id_type == "ISBN_13":
            return value
        if id_type == "ISBN_10" and isbn_10 is None:
            isbn_10 = value
    return isbn_10


def transform_google_book_item(item: dict[str, Any]) -> dict[str, Any]:
    """Transform a Google Books item to a Book-compatible payload."""
    volume_info = item.get("volumeInfo", {}) if isinstance(item, dict) else {}

    authors = volume_info.get("authors") or []
    if not isinstance(authors, list):
        authors = [str(authors)]

    categories = volume_info.get("categories") or []
    if not isinstance(categories, list):
        categories = [str(categories)]

    industry_identifiers = volume_info.get("industryIdentifiers") or []
    if not isinstance(industry_identifiers, list):
        industry_identifiers = []

    image_links = volume_info.get("imageLinks") or {}
    if not isinstance(image_links, dict):
        image_links = {}

    thumbnail = image_links.get("thumbnail") or image_links.get("smallThumbnail")

    return {
        "title": volume_info.get("title") or "Untitled",
        "authors": authors,
        "description": volume_info.get("description"),
        "language": volume_info.get("language"),
        "isbn": _extract_isbn(industry_identifiers),
        "thumbnail": thumbnail,
        "categories": categories,
        "is_indie": False,
    }
