"""Simple smoke test for the Book SQLAlchemy model."""

from flask import Flask

from extensions import db
from models import Book
from services.book_service import save_book


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books_test.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    return app


def run_test() -> None:
    app = create_app()

    with app.app_context():
        db.drop_all()
        db.create_all()

        sample_book_data = {
            "title": "The Indie Shelf",
            "authors": ["Patricia AlEs"],
            "description": "A sample book inserted by test script.",
            "language": "en",
            "isbn": "9780000000001",
            "thumbnail": "https://example.com/thumbnail.jpg",
            "categories": ["Fiction", "Indie"],
            "is_indie": True,
        }

        first_save = save_book(sample_book_data)
        second_save = save_book(sample_book_data)

        total_with_same_isbn = Book.query.filter_by(isbn=sample_book_data["isbn"]).count()
        reused_existing = first_save.id == second_save.id

        print("First save:", first_save)
        print("Second save:", second_save)
        print("Same record reused:", reused_existing)
        print("Rows with same ISBN:", total_with_same_isbn)
        print("Second call result JSON:", second_save.to_dict())


if __name__ == "__main__":
    run_test()
