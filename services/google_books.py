from __future__ import annotations

import re
from typing import Any

# Narrative-ish signals (case-insensitive).
_FANTASY_RE = re.compile(r"\bfantasy\b", re.IGNORECASE)
_FICTION_RE = re.compile(r"\bfiction\b", re.IGNORECASE)
_NONFICTION_RE = re.compile(
    r"\bnon[-\s]?fiction\b|\bnonfiction\b",
    re.IGNORECASE,
)

# Clearly non-narrative / non-target categories (substring match on full label).
_EXCLUDED_CATEGORY_SUBSTRINGS = (
    "guide",
    "guidebook",
    "handbook",
    "manual",
    "textbook",
    "technical",
    "programming",
    "computer software",
    "software development",
    "sports",
    "sport &",
    "catalog",
    "catalogue",
    "reference",
    "dictionary",
    "encyclopedia",
    "travel",
    "cookbook",
    "cooking",
    "self-help",
    "business",
    "economics",
    "law",
    "legal",
    "medical",
    "medicine",
    "mathematics",
    "transportation",
)

# Short tokens matched as whole words to avoid accidental substring hits.
_EXCLUDED_CATEGORY_WORDS = (
    "sport",
)

# Non-narrative signals in titles (substring match; title normalized to lowercase).
_EXCLUDED_TITLE_KEYWORDS = (
    "guide",
    "manual",
    "strategy",
    "official",
    "remake",
    "guía",
)


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


def _normalize_categories(volume_info: dict[str, Any]) -> list[str]:
    raw = volume_info.get("categories") or []
    if not isinstance(raw, list):
        return [str(raw)] if raw else []
    return [str(c) for c in raw if c is not None and str(c).strip()]


def _category_excluded(category: str) -> bool:
    c = category.lower()
    for needle in _EXCLUDED_CATEGORY_SUBSTRINGS:
        if needle in c:
            return True
    for word in _EXCLUDED_CATEGORY_WORDS:
        if re.search(rf"\b{re.escape(word)}\b", c):
            return True
    return False


def _has_fantasy_or_fiction_category(categories: list[str]) -> bool:
    for cat in categories:
        if _FANTASY_RE.search(cat):
            return True
        if _FICTION_RE.search(cat) and not _NONFICTION_RE.search(cat):
            return True
    return False


def _is_relevant_narrative_book(categories: list[str]) -> bool:
    if not categories:
        return False
    if any(_category_excluded(c) for c in categories):
        return False
    return _has_fantasy_or_fiction_category(categories)


def _title_excluded(title: str) -> bool:
    """Return True if the title should be skipped (keywords matched case-insensitively)."""
    t = (title or "").lower()
    return any(keyword in t for keyword in _EXCLUDED_TITLE_KEYWORDS)


def transform_google_book_item(item: dict[str, Any]) -> dict[str, Any] | None:
    """Transform a Google Books item to a Book-compatible payload, or None if skipped."""
    volume_info = item.get("volumeInfo", {}) if isinstance(item, dict) else {}

    categories = _normalize_categories(volume_info)
    if not _is_relevant_narrative_book(categories):
        return None

    title_raw = volume_info.get("title") or ""
    if _title_excluded(title_raw):
        return None

    authors = volume_info.get("authors") or []
    if not isinstance(authors, list):
        authors = [str(authors)]

    industry_identifiers = volume_info.get("industryIdentifiers") or []
    if not isinstance(industry_identifiers, list):
        industry_identifiers = []

    image_links = volume_info.get("imageLinks") or {}
    if not isinstance(image_links, dict):
        image_links = {}

    thumbnail = image_links.get("thumbnail") or image_links.get("smallThumbnail")

    return {
        "title": title_raw or "Untitled",
        "authors": authors,
        "description": volume_info.get("description"),
        "language": volume_info.get("language"),
        "isbn": _extract_isbn(industry_identifiers),
        "thumbnail": thumbnail,
        "categories": categories,
        "is_indie": False,
    }
