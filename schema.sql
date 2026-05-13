CREATE TABLE authors (
    author_id   INTEGER      PRIMARY KEY AUTOINCREMENT,
    first_name  VARCHAR(50)  NOT NULL,
    last_name   VARCHAR(50)  NOT NULL,
    birth_year  INTEGER
);

CREATE TABLE books (
    book_id          INTEGER      PRIMARY KEY AUTOINCREMENT,
    title            VARCHAR(200) NOT NULL,
    author_id        INTEGER      NOT NULL,
    genre            VARCHAR(50),
    total_copies     INTEGER      NOT NULL DEFAULT 1,
    available_copies INTEGER      NOT NULL DEFAULT 1,
    price            REAL         NOT NULL,
    FOREIGN KEY (author_id) REFERENCES authors(author_id)
);

CREATE TABLE members (
    member_id  INTEGER      PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(50)  NOT NULL,
    last_name  VARCHAR(50)  NOT NULL,
    email      VARCHAR(100) NOT NULL UNIQUE,
    phone      VARCHAR(20),
    join_date  DATE         NOT NULL DEFAULT (DATE('now'))
);

CREATE TABLE loans (
    loan_id     INTEGER     PRIMARY KEY AUTOINCREMENT,
    book_id     INTEGER     NOT NULL,
    member_id   INTEGER     NOT NULL,
    loan_date   DATE        NOT NULL,
    due_date    DATE        NOT NULL,
    return_date DATE,
    status      VARCHAR(20) NOT NULL DEFAULT 'active',
    FOREIGN KEY (book_id)   REFERENCES books(book_id),
    FOREIGN KEY (member_id) REFERENCES members(member_id)
);
