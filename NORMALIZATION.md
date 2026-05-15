# Normalization Report — Book Club Management System

## 1. Original Functional Dependencies

To demonstrate the normalization process, we start with a single flat table called `BOOK_CLUB_RECORD` that holds all book club data in one place.

| Column | Description |
|---|---|
| member_id | Unique ID for each member |
| member_first_name | Member's first name |
| member_last_name | Member's last name |
| member_email | Member's email (unique per person) |
| member_phone | Member's phone number |
| member_join_date | Date the member registered |
| book_title | Title of the book |
| book_author | Author of the book |
| book_genre | Genre of the book |
| book_publish_year | Year the book was published |
| book_total_pages | Total number of pages |
| book_isbn | Book's ISBN number |
| club_name | Name of the book club |
| club_description | Description of the club |
| club_city | City where the club is located |
| club_founded_date | Date the club was founded |
| membership_role | Member's role in the club (member/admin) |
| pages_read | Pages the member has read |
| read_status | Reading status (not_started, in_progress, completed) |
| completion_percentage | Percentage of the book completed |
| meeting_date | Date of a club meeting |
| meeting_location | Location of the meeting |
| meeting_notes | Notes from the meeting |
| review_rating | Member's rating of the book (1–5) |
| review_text | Member's written review |

**Functional dependencies identified in this flat table:**

- `member_id → member_first_name, member_last_name, member_email, member_phone, member_join_date`
- `member_email → member_first_name, member_last_name, member_phone, member_join_date`
- `book_isbn → book_title, book_author, book_genre, book_publish_year, book_total_pages`
- `club_name → club_description, club_city, club_founded_date`
- `member_id, club_name → membership_role`
- `member_id, book_isbn → pages_read, read_status, completion_percentage`
- `club_name, book_isbn, meeting_date → meeting_location, meeting_notes`
- `member_id, book_isbn → review_rating, review_text`

---

## 2. Anomaly Identification

### Update Anomaly
If a book's author name changes, every row in the table that references that book must be updated. If a club changes its city, every row containing that club's meetings and memberships must be updated. Missing even one row leaves the database inconsistent.

### Insertion Anomaly
A new book cannot be added until a member reads it or reviews it. A new club cannot be recorded until it has at least one member or meeting. There is no way to store an entity on its own without linking it to another.

### Deletion Anomaly
If the only review for a book is deleted, all information about that book is permanently lost. If the only meeting record for a club is deleted, all information about that club disappears with it.

---

## 3. Decomposition Steps

### Step 1 — Check 1st Normal Form (1NF)
**Rule:** All column values must be atomic and every row must be uniquely identifiable.

The flat `BOOK_CLUB_RECORD` table satisfies 1NF — all values are atomic and the combination of member, book, club, and date can identify each row.

**Result: Passes 1NF**

---

### Step 2 — Check 2nd Normal Form (2NF)
**Rule:** Every non-key column must depend on the whole primary key, not just part of it.

With a composite key across member, book, club, and date, many columns only partially depend on part of the key. For example, `book_author` only depends on the book, not on the member or club. `club_city` only depends on the club.

**Result: Fails 2NF — partial dependencies found**

---

### Step 3 — Check 3rd Normal Form (3NF)
**Rule:** No non-key column should depend on another non-key column.

Even after resolving partial dependencies, transitive dependencies remain:
- `member_id → member_email → member details` (email is also a unique identifier for a member)
- `book_isbn → book_title → book details` (ISBN uniquely identifies a book)

**Result: Fails 3NF — transitive dependencies found**

---

### Step 4 — Decompose into 3NF

**Extract Members**
```
members(member_id PK, first_name, last_name, email UNIQUE, phone, join_date, created_at)
```

**Extract Books**
```
books(book_id PK, title, author, genre, publish_year, total_pages, isbn, created_at)
```

**Extract Clubs**
```
clubs(club_id PK, club_name, description, city, founded_date, created_at)
```

**Extract Memberships** — resolves the many-to-many between members and clubs
```
memberships(membership_id PK, member_id FK, club_id FK, role, created_at)
```

**Extract Reading Progress** — tracks each member's progress on each book
```
reading_progress(progress_id PK, member_id FK, book_id FK, pages_read, status, started_date, finished_date, last_updated, completion_percentage)
```

**Extract Meetings** — ties a club to a book on a specific date
```
meetings(meeting_id PK, club_id FK, book_id FK, meeting_date, location, notes, created_at)
```

**Extract Reviews** — a member's rating and review of a book
```
reviews(review_id PK, member_id FK, book_id FK, rating, review_text, created_at)
```

---

## 4. Final Relational Schema (3NF)

```
BOOK_CLUB_RECORD (Unnormalized Flat Table)
│
│   member data, book data, club data,
│   membership role, reading progress,
│   meeting info, review rating and text
│
│   ↓ Remove member columns   → members table
│   ↓ Remove book columns     → books table
│   ↓ Remove club columns     → clubs table
│   ↓ Member ↔ Club link      → memberships table
│   ↓ Member ↔ Book progress  → reading_progress table
│   ↓ Club ↔ Book meeting     → meetings table
│   ↓ Member ↔ Book review    → reviews table
│
├── members
│   ├── member_id   (PK)
│   ├── first_name
│   ├── last_name
│   ├── email       (UNIQUE)
│   ├── phone
│   ├── join_date
│   └── created_at
│
├── books
│   ├── book_id      (PK)
│   ├── title
│   ├── author
│   ├── genre
│   ├── publish_year
│   ├── total_pages
│   ├── isbn
│   └── created_at
│
├── clubs
│   ├── club_id      (PK)
│   ├── club_name
│   ├── description
│   ├── city
│   ├── founded_date
│   └── created_at
│
├── memberships
│   ├── membership_id (PK)
│   ├── member_id     (FK → members)
│   ├── club_id       (FK → clubs)
│   ├── role
│   └── created_at
│
├── reading_progress
│   ├── progress_id           (PK)
│   ├── member_id             (FK → members)
│   ├── book_id               (FK → books)
│   ├── pages_read
│   ├── status
│   ├── started_date
│   ├── finished_date
│   ├── last_updated
│   └── completion_percentage
│
├── meetings
│   ├── meeting_id   (PK)
│   ├── club_id      (FK → clubs)
│   ├── book_id      (FK → books)
│   ├── meeting_date
│   ├── location
│   ├── notes
│   └── created_at
│
└── reviews
    ├── review_id   (PK)
    ├── member_id   (FK → members)
    ├── book_id     (FK → books)
    ├── rating      (CHECK 1–5)
    ├── review_text
    └── created_at
```

**Why this is in 3NF:**
- Each table has a single-column primary key.
- Every non-key attribute depends directly and only on that table's primary key.
- No table contains data about more than one real-world entity.
- All partial and transitive dependencies from the original flat table have been eliminated.
- The three anomalies no longer apply — members, books, and clubs each live in their own table and can be added, updated, or removed independently.
