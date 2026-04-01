"""SQLAlchemy models for the Flask application."""

from __future__ import annotations

from datetime import datetime, timezone

from extensions import db


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Book(db.Model):
    __tablename__ = "books"
    __table_args__ = (
        db.Index("ix_books_language_is_indie", "language", "is_indie"),
    )

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(512), nullable=False, index=True)
    authors = db.Column(db.JSON, nullable=False, default=list)
    description = db.Column(db.Text, nullable=True)
    language = db.Column(db.String(64), nullable=True, index=True)
    isbn = db.Column(db.String(32), unique=True, nullable=True)
    thumbnail = db.Column(db.String(2048), nullable=True)
    categories = db.Column(db.JSON, nullable=False, default=list)
    is_indie = db.Column(db.Boolean, nullable=False, default=False, index=True)
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=_utc_now,
        index=True,
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=_utc_now,
        onupdate=_utc_now,
    )

    def __repr__(self) -> str:
        return f"<Book id={self.id} title={self.title!r}>"

    def to_dict(self) -> dict:
        """Serialize the model for JSON APIs (datetimes as ISO 8601)."""
        return {
            "id": self.id,
            "title": self.title,
            "authors": self.authors if self.authors is not None else [],
            "description": self.description,
            "language": self.language,
            "isbn": self.isbn,
            "thumbnail": self.thumbnail,
            "categories": self.categories if self.categories is not None else [],
            "is_indie": self.is_indie,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
