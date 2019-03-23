import os
import json

from flask import Flask, session, request, redirect, render_template, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from passlib.apps import custom_app_context as pwd_context
from helpers import *

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "GET":
        return render_template("login.html", login_error=None)
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        db_lookup = db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).fetchone()
        if db_lookup is None or not pwd_context.verify(password, db_lookup.password):
            return render_template("login.html", login_error="Username and/or password invalid")
        session["user_id"] = db_lookup.id
        return redirect(url_for("index"))

@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", signup_error=None)
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        password_confirm = request.form.get("password-confirm")

        if db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).rowcount != 0:
            return render_template("register.html", signup_error="Username already exists")
        elif password != password_confirm:
            return render_template("register.html", signup_error="Passwords must match!")
        else:
            password_hash = pwd_context.hash(password)
            db.execute("INSERT INTO users (username, password) VALUES (:username, :password_hash)",\
                       {"username": username, "password_hash": password_hash})
            db.commit()
            session["user_id"] = db.execute("SELECT id FROM users WHERE username = :username",
                                 {"username": username}).fetchone().id
            return redirect(url_for("index"))

@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    if request.method == "GET":
        return redirect(url_for("index"))
    else:
        query = request.form.get("query")
        search_results = []
        for token in query.split():
            query_string = f"SELECT * FROM books JOIN authors \
                             ON authors.id = books.author_id WHERE \
                             isbn LIKE '%{token}%' OR \
                             LOWER(title) LIKE '%{token.lower()}%' OR \
                             LOWER(name) LIKE '%{token.lower()}%'"
            books = db.execute(query_string).fetchall()
            search_results += books
        return render_template("search.html", search_results=search_results)

@app.route("/book/<string:book_isbn>", methods=["GET", "POST"])
@login_required
def book(book_isbn):

    book = db.execute("SELECT title, name, year, isbn \
    FROM books JOIN authors \
    ON authors.id = books.author_id \
    WHERE isbn = :isbn",
    {"isbn": book_isbn}).fetchone()

    if request.method == "POST":
        rating = request.form.get("rating")
        review = request.form.get("review")
        db.execute("INSERT INTO reviews (review_isbn, user_id, rating, review) \
                    VALUES (:isbn, :id, :rating, :review)",
                    {"isbn": book.isbn, "id": session["user_id"], "rating": rating, "review":review})
        db.commit()

    # check if current user has already reviewed book
    reviewed = db.execute("SELECT * FROM reviews \
    WHERE user_id = :user AND review_isbn = :isbn",
    {"user": session["user_id"], "isbn": book.isbn}).fetchone()

    reviews = db.execute("SELECT rating, review, id \
    FROM reviews WHERE \
    review_isbn = :isbn \
    ORDER BY id DESC",
    {"user": session["user_id"], "isbn": book.isbn}).fetchall()
    return render_template("book.html", book=book, reviews=reviews, reviewed=reviewed)

@app.route("/api/<string:book_isbn>")
def api(book_isbn):
    book = db.execute("SELECT title, name, year, isbn \
                       FROM books JOIN authors \
                       ON authors.id = books.author_id \
                       WHERE isbn = :isbn",
                       {"isbn": book_isbn}).fetchone()

    review_count, avg_score = db.execute("SELECT COUNT(review), AVG(rating) \
                              FROM reviews \
                              WHERE review_isbn = :isbn",
                              {"isbn": book_isbn}).fetchone()
    book_info = {
        "title": book.title,
        "author": book.name,
        "year": book.year,
        "isbn": book.isbn,
        "review_count": review_count,
        "average_score": round(float(avg_score), 1)
    }
    return json.dumps(book_info)
