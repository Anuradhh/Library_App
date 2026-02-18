# 📚 Library Management System – Flask Web App

A simple Library Management System built using Flask and SQLAlchemy.  
This application helps manage books by adding, editing, borrowing, returning, deleting, and checking availability.

---

## 🚀 Features

- Add new books
- Prevent duplicate books
- Borrow and return books
- Edit book details
- Delete books
- Check availability
- Flash messages for feedback
- Clean user interface
- SQLite database support

---

## 🛠️ Technologies Used

- Python
- Flask
- SQLAlchemy
- SQLite
- HTML (Jinja2)
- CSS

---

## 📂 Project Structure
library_app/
│
├── app.py                     # Main Flask application
├── library.db                 # SQLite database (auto-created)
│
├── templates/                 # HTML templates
│   ├── index.html             # Home page
│   └── edit_book.html         # Edit book page
│
├── static/                    # Static files (CSS, images, etc.)
│   └── style.css              # Stylesheet
│
├── README.md                  # Project documentation
└── requirements.txt           # Project dependencies
