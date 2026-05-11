# Normalization Report — Library Management System

## 1. Original Functional Dependencies

To demonstrate the normalization process, we start with a single flat table called `LIBRARY_RECORD` that holds all library data in one place.

| Column | Description |
|---|---|
| loan_id | Unique ID for each loan |
| loan_date | Date the book was checked out |
| due_date | Date the book is due back |
| return_date | Date the book was returned (nullable) |
| loan_status | active or returned |
| book_title | Title of the book |
| book_genre | Genre of the book |
| book_total_copies | Total copies owned by the library |
| book_available_copies | Copies currently available to loan |
| book_price | Purchase price of the book |
| author_first_name | Author's first name |
| author_last_name | Author's last name |
| author_birth_year | Author's birth year |
| member_first_name | Member's first name |
| member_last_name | Member's last name |
| member_email | Member's email address (unique per person) |
| member_phone | Member's phone number |
| member_join_date | Date the member registered |

**Functional dependencies identified in this flat table:**

- `loan_id → loan_date, due_date, return_date, loan_status`
- `loan_id → book_title, book_genre, book_total_copies, book_available_copies, book_price`
- `loan_id → author_first_name, author_last_name, author_birth_year`
- `loan_id → member_first_name, member_last_name, member_email, member_phone, member_join_date`
- `book_title → book_genre, book_price, author_first_name, author_last_name, author_birth_year`
- `member_email → member_first_name, member_last_name, member_phone, member_join_date`

---

## 2. Anomaly Identification

### Update Anomaly
If an author changes their name, every single row in the table that contains a book by that author must be updated. If even one row is missed, the database becomes inconsistent — two rows now show different names for the same author.

### Insertion Anomaly
A new book or author cannot be added to the system until at least one loan is created for it. There is no way to record a book that no one has borrowed yet. Likewise, a new member cannot be recorded until they borrow a book.

### Deletion Anomaly
If the only loan for a particular book is deleted, all information about that book and its author is permanently lost. The deletion of one loan record unintentionally destroys unrelated data.

---

## 3. Decomposition Steps

### Step 1 — Check 1st Normal Form (1NF)
**Rule:** All column values must be atomic (no lists, sets, or repeating groups), and every row must be uniquely identifiable by a primary key.

The flat `LIBRARY_RECORD` table satisfies 1NF — every value is a single atomic value and `loan_id` serves as the primary key.

**Result: Passes 1NF**

---

### Step 2 — Check 2nd Normal Form (2NF)
**Rule:** Every non-key column must depend on the *whole* primary key, not just part of it (no partial dependencies).

Because `loan_id` is a single-column primary key, partial dependencies cannot exist by definition — you cannot have a dependency on only part of a one-column key.

**Result: Passes 2NF**

---

### Step 3 — Check 3rd Normal Form (3NF)
**Rule:** No non-key column should depend on another non-key column (no transitive dependencies).

Two transitive dependency chains were found:

**Chain 1:**
```
loan_id → book_title → author_first_name, author_last_name, author_birth_year
```
Author information depends on the book, not directly on the loan. The author columns are in the table only because a book is in the table.

**Chain 2:**
```
loan_id → member_email → member_first_name, member_last_name, member_phone, member_join_date
```
Member details depend on the member's identity, not directly on the loan record.

**Result: Fails 3NF — decomposition required**

---

### Step 4 — Decompose into 3NF

**Extract Authors**

Remove all author columns from the flat table and create a dedicated `authors` table with its own primary key.

```
authors(author_id PK, first_name, last_name, birth_year)
```

**Extract Books**

Remove all book columns and create a `books` table. Use `author_id` as a foreign key instead of repeating author data in every row.

```
books(book_id PK, title, author_id FK, genre, total_copies, available_copies, price)
```

> Note on `available_copies`: This column is stored explicitly rather than being computed from the loans table on every query. This is a deliberate performance trade-off. The application keeps it in sync during checkout and return transactions — if either step fails, neither is saved.

**Extract Members**

Remove all member columns and create a `members` table. The `email` column is enforced as unique since no two members share an email address.

```
members(member_id PK, first_name, last_name, email UNIQUE, phone, join_date)
```

**Remaining Loans Table**

Replace all the embedded book and member data with foreign keys pointing to their respective tables.

```
loans(loan_id PK, book_id FK, member_id FK, loan_date, due_date, return_date, status)
```

---

## 4. Final Relational Schema (3NF)

```
authors(author_id PK, first_name, last_name, birth_year)

books(book_id PK, title, author_id FK → authors, genre, total_copies, available_copies, price)

members(member_id PK, first_name, last_name, email UNIQUE, phone, join_date)

loans(loan_id PK, book_id FK → books, member_id FK → members, loan_date, due_date, return_date, status)
```

**Why this is in 3NF:**
- Each table has a single-column primary key.
- Every non-key attribute in each table depends directly and only on that table's primary key.
- No table contains data about more than one real-world entity.
- All transitive dependencies from the original flat table have been eliminated.
- The three original anomalies (update, insert, delete) no longer apply — authors, books, and members each live in their own table and can be added, changed, or removed independently.
