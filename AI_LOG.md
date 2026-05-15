# AI Assistance Log

This file documents every instance of AI assistance used in this project, as required by course policy.

---

## Research: Normalization Ideas for a Book Club Project

**Tool:** Claude

**Prompt:**
"Give me some ideas for how to apply normalization to a book club database project. What would an unnormalized version look like and how would I break it down into 3NF?"

**AI Output:**
Claude explained the concept of starting with a single flat table that combines member, book, club, membership, reading progress, meeting, and review data into one row. It described the three types of anomalies that would result (update, insertion, deletion), then walked through how to identify partial and transitive dependencies and split the table into smaller, cleaner tables to reach 3NF. It also provided this decomposition tree as a visual guide:

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

**My Modification:**
I used these ideas as a guide to analyze my own schema from Project 2. I applied the concepts to my specific tables (embers, books, clubs, memberships, reading_progress, meetings, reviews and confirmed that my design already satisfied 3NF.
---

## Frontend: HTML Templates

**Tool:** Claude

**Prompt:**
"Help me generate the HTML templates for my book club app. I need pages for listing clubs, a club detail page showing members and meetings, a form for adding members to clubs, a reading progress list and log form, a reviews page and form, and a meetings page and form. Use Bootstrap and follow the same style as the existing pages."

**AI Output:**
Claude generated the HTML for all templates including `clubs.html`, `club_form.html`, `club_detail.html`, `join_form.html`, `progress.html`, `progress_form.html`, `reviews.html`, `review_form.html`, `meetings.html`, and `meeting_form.html`. Each template extends the base layout, uses Bootstrap tables, cards, and form components, and includes status badges for reading progress (Not Started, In Progress, Completed) and star ratings for reviews.

**My Modification:**
I reviewed each template and adjusted the fields and labels to match my actual database columns. I verified that the form name attributes matched the field names my Flask routes were expecting, and confirmed that the progress bar and star rating display matched the data stored in the database.

---

## Documentation: NORMALIZATION.md and README.md

**Tool:** Claude

**Prompt:**
"Help me write the NORMALIZATION.md and README.md files for my book club project. The normalization report needs to show the original flat schema, functional dependencies, anomalies, decomposition steps, and the final 3NF schema with a tree diagram. The README needs installation instructions, database setup, and a usage guide for all features."

**AI Output:**
Claude generated both documents. The NORMALIZATION.md followed the structure I outlined using the book club schema with all 7 tables, and the README.md included sections for project description, tech stack, installation steps for Windows and Mac, database setup, a full feature walkthrough, project structure, and a deliverables table.

**My Modification:**
I read through both documents and verified that they accurately described my actual project. I confirmed the normalization decomposition matched my real table structure and that the anomaly examples made sense in the context of a book club system.

---

## Syntax and Logic Review

**Tool:** Claude

**Prompt:**
"Check the syntax and logic of the code I just implemented"

**AI Output:**
Claude reviewed the code and identified issues including typos in the original SQL schema wrong column names in foreign keys for reviews and meetings tables, a misspelled table name, and suggested fixes to align the Flask models with the correct intended structure.

**My Modification:**
I read through each suggestion and verified whether it applied to my specific use case before accepting it. I confirmed the foreign key corrections were accurate by cross-referencing with my original SQL insert statements.
