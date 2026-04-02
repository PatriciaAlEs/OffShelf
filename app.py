from __future__ import annotations

from flask import Flask
from flask_cors import CORS

from extensions import db
from routes.books import books_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    CORS(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(books_bp)

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
