import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    current_cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
    stock_symbols = db.execute("SELECT symbol FROM portfolio WHERE user_id = :user_id GROUP BY symbol",
                        user_id=session["user_id"])
    grand_total = 0

    if stock_symbols != []:
        stocks = []
        for symbol in stock_symbols:
            symbol_data = lookup(symbol["symbol"])
            stock_shares = db.execute("SELECT TOTAL(shares) FROM portfolio WHERE user_id=:user_id AND symbol=:symbol;",
            user_id=session["user_id"], symbol=symbol_data["symbol"])
            if stock_shares[0]["TOTAL(shares)"] == 0:
                continue
            else:
                stock_info = {}

                stock_info["name"] = symbol_data["name"]
                stock_info["symbol"] = symbol_data["symbol"]
                stock_info["price"] = symbol_data["price"]
                stock_info["shares"] = stock_shares[0]["TOTAL(shares)"]
                stock_info["total"] = stock_info["shares"] * stock_info["price"]

                stocks.append(stock_info)

        for i in range(len(stocks)):
            grand_total += stocks[i]["total"]

        grand_total += current_cash[0]["cash"]

        for i in range(len(stocks)):
            stocks[i]["price"] = usd(stocks[i]["price"])
            stocks[i]["total"] = usd(stocks[i]["total"])

        return render_template("index.html", stocks=stocks, current_cash=usd(current_cash[0]["cash"]), grand_total=usd(grand_total))
    else:
        current_cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
        return render_template("index.html", current_cash=usd(current_cash[0]["cash"]), grand_total=usd(current_cash[0]["cash"]))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        small_symbol = request.form.get("symbol")
        big_symbol = small_symbol.upper()
        quote = lookup(big_symbol)
        shares = int(request.form.get("shares"))

        if not quote or not shares:
            return apology("Must enter a symbol and/or number of shares.", 400)
        if quote == None:
            return apology("That symbol is invalid.", 400)
        if shares <= 0:
            return apology("Must enter a positive integer.", 400)

        # look for the current user's cash amount
        rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])

        cash_remaining = rows[0]["cash"]
        stock_price = quote["price"]

        total_price = stock_price * shares

        if cash_remaining < total_price:
            return apology("You do not have enough to make this purchase.", 400)

        # keep track of what they have left
        db.execute("UPDATE users SET cash = cash - :price WHERE id = :user_id", user_id=session["user_id"], price=total_price)

        # add this transaction into the portfolio table
        db.execute("INSERT INTO portfolio (user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)",
                    user_id=session["user_id"], symbol=big_symbol, shares=shares, price=stock_price)

        flash("Purchase successful!")

        return redirect(url_for("index"))

    else:
        return render_template("buy.html")

@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    """Change password"""
    if request.method == "POST":

        old_password = request.form.get("old_pass")
        if not old_password: # if they leave the space blank, return apology
            return apology("Must provide old password", 403)

        rows = db.execute("SELECT hash FROM users WHERE id = :user_id", user_id=session["user_id"])

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], old_password):
            return apology("Invalid password", 400)

        new_password = request.form.get("new_pass")
        if not new_password:
            return apology("Must provide a new password", 403)

        new_pass_confirm = request.form.get("new_pass_confirm")
        if not new_pass_confirm:
            return apology("Must confirm the new password", 403)

        # if passwords do not match
        if new_password != new_pass_confirm:
            return apology("New passwords do not match", 403)

        # hash the password for security
        new_hashedpass = generate_password_hash(new_password)

        # insert the new user into the table
        updated_password = db.execute("UPDATE users SET hash = :hash WHERE id = :user_id", user_id=session["user_id"], hash=new_hashedpass)

        flash("You have changed your password.")

        # automatically log them in instead of directing them to the login page
        return redirect(url_for("index"))

    else:
        return render_template("change.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    stocks = db.execute("SELECT symbol, shares, price, timewhen FROM portfolio WHERE user_id = :user_id ORDER BY timewhen",
                        user_id=session["user_id"])

    for stock in stocks:
        stock["price"] = usd(stock["price"])

    return render_template("history.html", stocks=stocks)



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))
        if quote == None:
            return apology("That symbol is invalid.")

        return render_template("quoted.html", quote=quote)

    # user tries to GET the page
    else:
        return render_template("quote.html")


# Allow a new user to register themselves into the system
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        if not username: # if they leave the space blank, return an apology
            return apology("Must provide a username", 403)

        # check to ensure the username is unique and doesn't already exist in the table
        checkuser = db.execute("SELECT * FROM users WHERE username = :username", username=username)
        if checkuser == 1:
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
        new_user_id = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=username, hash=hashedpass)

        flash("You have registered successfully.")
        session["user_id"] = new_user_id

        # automatically log them in instead of directing them to the login page
        return redirect(url_for("index"))

    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        small_symbol = request.form.get("symbol")
        big_symbol = small_symbol.upper()
        quote = lookup(big_symbol)
        shares = int(request.form.get("shares"))

        if not quote or not shares:
            return apology("Must enter a symbol and/or number of shares.", 400)
        if quote == None:
            return apology("That symbol is invalid.", 400)
        if shares <= 0:
            return apology("Must enter a positive integer.", 400)

        stocks = db.execute("SELECT TOTAL(shares) as total_shares FROM portfolio WHERE user_id = :user_id AND symbol = :symbol",
                          user_id=session["user_id"], symbol=big_symbol)
        if len(stocks) != 1 or stocks[0]["total_shares"] < shares:
            return apology("You cannot sell less than 0 shares or more shares than you own.", 400)

        # look for the current user's cash amount
        rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])

        cash_remaining = rows[0]["cash"]
        stock_price = quote["price"]

        total_price = stock_price * shares

        if cash_remaining < total_price:
            return apology("You do not have enough to make this purchase.", 400)

        # keep track of what they have left
        db.execute("UPDATE users SET cash = cash + :price WHERE id = :user_id", user_id=session["user_id"], price=total_price)

        # add this transaction into the portfolio table
        db.execute("INSERT INTO portfolio (user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)",
                    user_id=session["user_id"], symbol=request.form.get("symbol"), shares=-shares, price=stock_price)

        flash("Successfully sold.")

        return redirect(url_for("index"))

    else:
        return render_template("sell.html")



def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
