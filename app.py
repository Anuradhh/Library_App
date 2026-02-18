from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = "library_secret"

# Database setup
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "library.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default="Available")

    def __repr__(self):
        return f"<Book {self.title}>"

# Home page
@app.route("/")
def index():
    books = Book.query.all()
    return render_template("index.html", books=books)

# Add new book
@app.route("/add_book", methods=["POST"])
def add_book():
    title = request.form.get("title").strip()
    author = request.form.get("author").strip()

    if not title or not author:
        flash("Please fill in all fields!", "error")
        return redirect(url_for("index"))

    # ✅ Check for duplicate (case-insensitive match)
    existing_book = Book.query.filter(
        db.func.lower(Book.title) == title.lower(),
        db.func.lower(Book.author) == author.lower()
    ).first()

    if existing_book:
        flash(f"The book '{title}' by {author} already exists in the library.", "error")
        return redirect(url_for("index"))

    # ✅ Add only if not duplicate
    new_book = Book(title=title, author=author, status="Available")
    db.session.add(new_book)
    db.session.commit()
    flash(f"Book '{title}' added successfully!", "success")
    return redirect(url_for("index"))


# Borrow a book
@app.route("/borrow_book/<int:book_id>")
def borrow_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.status == "Available":
        book.status = "Borrowed"
        db.session.commit()
        flash(f"You borrowed '{book.title}'", "success")
    else:
        flash("Book already borrowed!", "error")
    return redirect(url_for("index"))

# Return a borrowed book
@app.route("/return_book/<int:book_id>")
def return_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.status == "Borrowed":
        book.status = "Available"
        db.session.commit()
        flash(f"You returned '{book.title}'", "success")
    else:
        flash("Book is not borrowed!", "error")
    return redirect(url_for("index"))

# Delete a book
@app.route("/delete_book/<int:book_id>")
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash(f"Book '{book.title}' removed successfully!", "error")
    return redirect(url_for("index"))

# Edit a book (GET shows form, POST saves changes)
@app.route("/edit_book/<int:book_id>", methods=["GET", "POST"])
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == "POST":
        new_title = request.form.get("title")
        new_author = request.form.get("author")
        if not new_title or not new_author:
            flash("Please fill in all fields!", "error")
        else:
            book.title = new_title
            book.author = new_author
            db.session.commit()
            flash(f"Book '{book.title}' updated successfully!", "success")
            return redirect(url_for("index"))
    # GET request → render edit form
    return render_template("edit_book.html", book=book)

# Check book availability
@app.route("/check_book", methods=["POST"])
def check_book():
    title = request.form.get("search_title")
    book = Book.query.filter(Book.title.ilike(f"%{title}%")).first()
    if book:
        flash(f"'{book.title}' is {book.status}.", "info")
    else:
        flash(f"'{title}' not found in library.", "error")
    return redirect(url_for("index"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

