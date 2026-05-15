# Book Club Management System

A web application for managing book clubs, members, reading progress, and reviews. Built with Python and Flask, it lets book club organizers track members, schedule meetings, log reading progress, and collect book reviews.

---

## Project Description

This app is designed for book club organizers who need a simple way to:

- Manage members and their club memberships
- Keep a catalog of books being read
- Create and manage book clubs
- Schedule and track club meetings
- Log reading progress for each member
- Collect and display book reviews and ratings
- View a dashboard with key stats about the club activity

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
py -m venv venv
venv\Scripts\Activate.ps1

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

The app uses SQLite

```
schema.sql
```

It contains all seven `CREATE TABLE` statements reflecting the final 3NF structure.

---

## Usage

**Start the server**
```bash
py app.py
```

Then open your browser and go to: `http://127.0.0.1:5000`

---

## Features

### Dashboard
The home page displays a live summary of all club activity:
- Total members, books, clubs, and reviews
- Number of books completed and currently being read
- Average book rating across all reviews

### Books
- View all books with author, genre, publish year, and page count
- Add, edit, and delete books
- Click a book to see its full detail page with all reviews

### Clubs
- View all clubs with member count and founding date
- Add, edit, and delete clubs
- Click a club to see its members and scheduled meetings

### Members
- View all registered members and how many clubs they belong to
- Add, edit, and delete members

### Memberships
- Add a member to a club with a role (member or admin)
- Remove a member from a club from the club detail page

### Reading Progress
- Log how many pages a member has read for a book
- Set reading status: Not Started, In Progress, or Completed
- Completion percentage is calculated and saved automatically in a single transaction

### Reviews
- Add a star rating (1–5) and written review for any book
- View all reviews sorted by newest first
- Delete reviews

### Meetings
- Schedule a meeting for a club tied to a specific book
- Add location and discussion notes
- View all upcoming and past meetings

---

## Project Structure

```
database_project/
├── app.py              # All Flask routes
├── models.py           # SQLAlchemy models
├── schema.sql          # SQL schema (3NF)
├── requirements.txt    # Python dependencies
├── NORMALIZATION.md    # Normalization report
├── AI_LOG.md           # AI assistance log
├── static/
│   └── style.css
└── templates/
    ├── base.html
    ├── dashboard.html
    ├── books.html
    ├── book_form.html
    ├── book_detail.html
    ├── clubs.html
    ├── club_form.html
    ├── club_detail.html
    ├── members.html
    ├── member_form.html
    ├── join_form.html
    ├── progress.html
    ├── progress_form.html
    ├── reviews.html
    ├── review_form.html
    ├── meetings.html
    └── meeting_form.html
```
