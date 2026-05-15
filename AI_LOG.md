# AI Assistance Log

This file documents every instance of AI assistance used in this project, as required by course policy.

---

## Research: Normalization Ideas for a Library Project

**Tool:** Claude

**Prompt:**
 "Give me some ideas for how to apply normalization to a library database project. What would an unnormalized version look like and how would I break it down into 3NF?"

**AI Output:**
Claude explained the concept of starting with a single flat table that combines loan, book, author, and member data into one row. It described the three types of anomalies that would result (update, insertion, deletion), then walked through how to identify transitive dependencies and split the table into smaller, cleaner tables to reach 3NF. It also provided this decomposition tree as a visual guide:

```
LIBRARY_RECORD (Unnormalized Flat Table)
│
│   loan_id, loan_date, due_date, return_date, status
│   book_title, book_genre, book_total_copies, book_available_copies, book_price
│   author_first_name, author_last_name, author_birth_year
│   member_first_name, member_last_name, member_email, member_phone, member_join_date
│
│   ↓ Remove author columns → authors table
│   ↓ Remove book columns   → books table (references authors)
│   ↓ Remove member columns → members table
│   ↓ Keep only loan data   → loans table (references books + members)
│
├── authors
│   ├── author_id  (PK)
│   ├── first_name
│   ├── last_name
│   └── birth_year
│
├── books
│   ├── book_id        (PK)
│   ├── title
│   ├── author_id      (FK → authors)
│   ├── genre
│   ├── total_copies
│   ├── available_copies
│   └── price
│
├── members
│   ├── member_id  (PK)
│   ├── first_name
│   ├── last_name
│   ├── email      (UNIQUE)
│   ├── phone
│   └── join_date
│
└── loans
    ├── loan_id     (PK)
    ├── book_id     (FK → books)
    ├── member_id   (FK → members)
    ├── loan_date
    ├── due_date
    ├── return_date
    └── status
```

**My Modification:**
I used these ideas as a guide to analyze my own schema. I applied the concepts to my specific tables authors, books, members, loans and confirmed that my design already satisfied 3NF. I then wrote the code based on my own understanding.

---

## Frontend: HTML Templates

**Tool:** Claude

**Prompt:**
"Help me generate the HTML templates for my library app. I need pages for listing members, a form for adding and editing members, a loans list page, and a checkout form. Use Bootstrap and follow the same style as the existing authors and books pages"

**AI Output:**
Claude generated the HTML for `members.html`, `member_form.html`, `loans.html`, and `checkout_form.html`. Each template extends the base layout, uses Bootstrap tables and form components, and includes buttons for actions like edit, delete, checkout, and return.

**My Modification:**
I reviewed each template and adjusted the fields and labels to match my actual database columns. I also checked that the form name attributes matched the field names my Flask routes were expecting.

---

## Documentation: NORMALIZATION.md and README.md

**Tool:** Claude 

**Prompt:**
"Help me write the NORMALIZATION.md and README.md files for my library project"

**AI Output:**
Claude generated both documents. The NORMALIZATION.md followed the structure I outlined, and the README.md included sections for project description, tech stack, installation steps, database setup, and a feature walkthrough.

**My Modification:**
I read through both documents and verified that they accurately described my actual project. 

## Syntax and logic

**Tool:** Claude 

**Prompt:**
"Check the syntax and logic of the code I just implemented"

**AI Output:**
check the code and suggest the fix

**My Modification:**
read the suggestion and understand it. Then verity if that suggestion fit with my use
