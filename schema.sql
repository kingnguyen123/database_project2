-- Book Club Management System
-- Final Schema in 3rd Normal Form
-- Database: SQLite

CREATE TABLE members (
    member_id  INTEGER       PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(50)   NOT NULL,
    last_name  VARCHAR(50)   NOT NULL,
    email      VARCHAR(100)  NOT NULL UNIQUE,
    phone      VARCHAR(20),
    join_date  DATE          NOT NULL,
    created_at TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE books (
    book_id      INTEGER      PRIMARY KEY AUTOINCREMENT,
    title        VARCHAR(200) NOT NULL,
    author       VARCHAR(100) NOT NULL,
    genre        VARCHAR(50),
    publish_year SMALLINT,
    total_pages  SMALLINT,
    isbn         VARCHAR(20),
    created_at   TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE clubs (
    club_id      INTEGER       PRIMARY KEY AUTOINCREMENT,
    club_name    VARCHAR(100)  NOT NULL,
    description  VARCHAR(1000),
    city         VARCHAR(80),
    founded_date DATE          NOT NULL,
    created_at   TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE memberships (
    membership_id INTEGER     PRIMARY KEY AUTOINCREMENT,
    member_id     INTEGER     NOT NULL,
    club_id       INTEGER     NOT NULL,
    role          VARCHAR(30) DEFAULT 'member',
    created_at    TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE CASCADE,
    FOREIGN KEY (club_id)   REFERENCES clubs(club_id)   ON DELETE CASCADE
);

CREATE TABLE reading_progress (
    progress_id           INTEGER      PRIMARY KEY AUTOINCREMENT,
    member_id             INTEGER      NOT NULL,
    book_id               INTEGER      NOT NULL,
    pages_read            SMALLINT     DEFAULT 0,
    status                VARCHAR(20)  DEFAULT 'not_started',
    started_date          DATE,
    finished_date         DATE,
    last_updated          TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    completion_percentage DECIMAL(5,2),
    FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE CASCADE,
    FOREIGN KEY (book_id)   REFERENCES books(book_id)     ON DELETE CASCADE
);

CREATE TABLE meetings (
    meeting_id   INTEGER       PRIMARY KEY AUTOINCREMENT,
    club_id      INTEGER       NOT NULL,
    book_id      INTEGER       NOT NULL,
    meeting_date DATE          NOT NULL,
    location     VARCHAR(150),
    notes        VARCHAR(1000),
    created_at   TIMESTAMP     DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (club_id)  REFERENCES clubs(club_id) ON DELETE CASCADE,
    FOREIGN KEY (book_id)  REFERENCES books(book_id) ON DELETE CASCADE
);

CREATE TABLE reviews (
    review_id   INTEGER      PRIMARY KEY AUTOINCREMENT,
    member_id   INTEGER      NOT NULL,
    book_id     INTEGER      NOT NULL,
    rating      SMALLINT     CHECK(rating BETWEEN 1 AND 5),
    review_text VARCHAR(1000),
    created_at  TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE CASCADE,
    FOREIGN KEY (book_id)   REFERENCES books(book_id)     ON DELETE CASCADE
);
