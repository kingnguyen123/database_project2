# Library Management System

A web application for managing a library's books, authors, members, and loan records. Built with Python and Flask, it lets library staff track inventory, register members, and handle book checkouts and returns.

---

## Project Description

This app is designed for small library staff who need a simple way to:

- Keep track of books and their authors
- Register and manage library members
- Check out books to members and record returns
- View a dashboard with key stats like active loans, overdue books, and inventory value

The database is normalized to **3rd Normal Form** — see [NORMALIZATION.md](NORMALIZATION.md) for the full report.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3 |
| Framework | Flask |
| Database | SQLite |
| ORM | SQLAlchemy |
| Frontend | HTML5, Bootstrap 5, Jinja2 |

---

## Installation

**1. Clone the repository**
```bash
git clone <your-repo-url>
cd database_project
```

**2. Create and activate a virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

---

## Database Setup

The app uses SQLite. The database file (`library.db`) is created automatically the first time you run the app — no manual setup needed.

If you want to review the schema, the SQL file is included in the repository:

```
schema.sql
```

It contains all four `CREATE TABLE` statements reflecting the final 3NF structure.

---

## Usage

**Start the server**
```bash
python app.py
```

Then open your browser and go to: `http://127.0.0.1:5000`

---

## Features

### Dashboard
The home page displays a live summary of the library:
- Total books, authors, members, and loans
- Number of active and overdue loans
- Average book price and total inventory value

### Books
- View all books with availability status
- Add, edit, and delete books
- Each book is linked to an author

### Authors
- View all authors and how many books they have
- Add, edit, and delete authors
- An author cannot be deleted if they have books in the system

### Members
- View all registered members
- Add, edit, and delete members
- A member cannot be deleted if they have any loan history

### Loans
- Check out a book to a member (14-day loan period)
- Return a book when it comes back
- See loan status: Active, Overdue, or Returned
- Checkout and return each use a database transaction — both the loan record and the book's availability are updated together



