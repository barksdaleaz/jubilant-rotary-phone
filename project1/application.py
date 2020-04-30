import os
import psycopg2
import requests
import json

from cs50 import sql

from flask import flash, Flask, session, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash

from project1helpers import apology, login_required
# import requests

app = Flask(__name__)

# Check for environment variable # used to be "DATABASE_URL"
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
def index():
    return render_template("index1.html")

# Allow a new user to register themselves into the system
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username1 = request.form.get("username")
        if not username1: # if they leave the space blank, return an apology
            return apology("Must provide a username", 403)

        # check to ensure the username is unique and doesn't already exist in the table
        checkuser = db.execute("SELECT * FROM users WHERE username = :username", {"username": username1}).fetchone()
        if checkuser:
            flash("This username already exists. Please try again.")
            return apology("That username already exists. Please try again.", 403)

        password = request.form.get("password")
        if not password: # if they leave the space blank, return apology
            return apology("Must provide a password", 403)

        confirmation = request.form.get("confirmation")
        if not confirmation:
            return apology("Must confirm password", 403)

        # if passwords do not match
        if password != confirmation:
            return apology("Passwords do not match", 403)

        # hash the password for security
        hashedpass = generate_password_hash(request.form.get("password"))

        # insert the new user into the table
        new_user_id = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", {"username": username1, "hash": hashedpass})
        db.commit()
        # db.close()

        flash("You have registered successfully.")
        # session["user_id"] = new_user_id

        # automatically log them in instead of directing them to the login page
        return redirect("/login")

    else:
        return render_template("project1register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username1 = request.form.get("username1")
        password1 = request.form.get("password")
        # Ensure username was submitted
        if not request.form.get("username1"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not password1:
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", {"username": username1})
        user = rows.fetchone()
        # Ensure username exists and password is correct
        if not user:
            return apology("Invalid username", 403)

        current_user_hash = db.execute("SELECT hash FROM users WHERE username = :username", {"username": username1}).fetchone()
        current_user_id = db.execute("SELECT id FROM users WHERE username = :username", {"username": username1}).fetchone()

        # if not check_password_hash(current_user_hash, password1):
            # return apology("Invalid password", 403)

        # Remember which user has logged in
        session["user_id"] = current_user_id

        # Redirect user to home page
        return redirect("/search")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    """Searching for a book"""
    if request.method == "POST":
        query = "%" + request.form.get("search") + "%"
        if not request.form.get("search"):
            return apology("Please input an ISBN, title, or author", 403)
        # query = query.title()
        sql_string = "SELECT isbn, title, author, year FROM books3 WHERE (isbn LIKE :query OR title ILIKE :query OR author ILIKE :query OR CAST (year AS VARCHAR(4)) LIKE :query)"

        # Query database for searched item
        rows = db.execute(sql_string, {"query": query})


        books = rows.fetchall()
        if rows == 0:
            return apology("Book not found.", 403)

        return render_template("project1searchresults.html", books=books)

    else:
        return render_template("project1search.html")

@app.route("/book/<string:isbn>", methods=["GET", "POST"])
@login_required
def book(isbn):

    if request.method == "POST":
        currentuser = session["user_id"]
        review = request.form.get("review")
        rating = request.form.get("rating")
        # date = datetime.now()

        # find book_id by isbn
        row = db.execute("SELECT id FROM books3 WHERE isbn = :isbn", {"isbn":isbn}).fetchone()
        bookid = row[0]

        # check if the user has already made a review for this

        row2 = db.execute("SELECT * FROM reviews WHERE user_id = :user_id AND book_id = :book_id", {"user_id": currentuser[0], "book_id": bookid}).fetchone()
        if row2:
            #flash("You already submitted a review for this book.")
            return apology("You have already submitted a review for this book", 403)

        #get user_id to get # REVIEW
        rating = int(rating)

        db.execute("INSERT INTO reviews (rating, review, book_id, user_id)\
                    VALUES (:rating, :review, :book_id, :user_id)",
                    {"rating": rating,
                    "review": review,
                    "book_id": bookid,
                    "user_id": currentuser[0]})

        db.commit()

        flash("Review submitted!")
        return redirect("/book/" + isbn)
    else:

        # GOODREADS_KEY = 7GR3JHJ6CRqf0kwkAtlpAA
        # read API key from goodreads
        key = os.getenv("GOODREADS_KEY")
        # search book ID using isbn
        book = db.execute("SELECT * FROM books3 WHERE isbn = :isbn", {"isbn": isbn})
        bookinfo = book.fetchall()

        # import API from Goodreads
        r = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": key, "isbns": isbn})
        r.raise_for_status()

        goodinfo = r.json()
        scratch = goodinfo["books"][0]
        bookinfo.append(scratch)
        reviews_count = bookinfo[1]["work_ratings_count"]
        average_rating = bookinfo[1]["average_rating"]

        bookinfo.append(scratch)

        if r.status_code != 200:
          raise ValueError

        book1 = db.execute("SELECT id FROM books3 WHERE isbn = :isbn", {"isbn": isbn}).fetchone()[0]

        results = db.execute("SELECT username, rating, review FROM users INNER JOIN reviews ON users.id = reviews.user_id WHERE book_id = :book", {"book": book1})
        allreviews = results.fetchall()

        return render_template("project1results.html", reviews_count=reviews_count, average_rating=average_rating, reviews=allreviews, bookinfo=bookinfo)

@app.route("/api/<string:isbn>", methods=["GET"])
@login_required
def api(isbn):
    # find that specific book with all the information
    # used the id from reviews to count all the reviews
    # used AVG to create an average of the ratings from reviews TABLE
    # get data from database
    rows = db.execute("SELECT title, author, year, isbn \
        FROM books3 WHERE isbn = :isbn", {"isbn": isbn})

    if rows.rowcount != 1:
        return apology("The ISBN you entered is invalid.", 404)

    # turn the data into a dict
    book_data = dict(rows.first())
    book_data['isbn'] = isbn

    # get reviews count and average reviews from Goodreads via API
    key = os.getenv("GOODREADS_KEY")
    r = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": key, "isbns": isbn})
    r.raise_for_status()

    book = db.execute("SELECT * FROM books3 WHERE isbn = :isbn", {"isbn": isbn})
    bookinfo = book.fetchall()
    goodinfo = r.json()
    scratch = goodinfo["books"][0]
    bookinfo.append(scratch)
    reviews_count = bookinfo[1]["work_ratings_count"]
    average_rating = bookinfo[1]["average_rating"]

    # turn into dict
    result = {"reviews_count": reviews_count, "average_rating": average_rating}

    # put Goodreads data into book_data from the database
    book_data["average_rating"] = result["average_rating"]
    book_data["reviews_count"] = result["reviews_count"]

    # Round Avg Score to 2 decimal. This returns a string which does not meet the requirement.
    # https://floating-point-gui.de/languages/python/
    # result['average_score'] = float('%.2f'%(result['average_score']))

    book_json = json.dumps(book_data, )
    return book_json
