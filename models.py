from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

db = SQLAlchemy()


class Member(db.Model):
    __tablename__ = 'members'

    member_id  = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name  = db.Column(db.String(50), nullable=False)
    email      = db.Column(db.String(100), nullable=False, unique=True)
    phone      = db.Column(db.String(20))
    join_date  = db.Column(db.Date, nullable=False, default=date.today)
    created_at = db.Column(db.DateTime, default=datetime.now)

    memberships      = db.relationship('Membership', backref='member', lazy=True)
    reading_progress = db.relationship('ReadingProgress', backref='member', lazy=True)
    reviews          = db.relationship('Review', backref='member', lazy=True)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Book(db.Model):
    __tablename__ = 'books'

    book_id      = db.Column(db.Integer, primary_key=True)
    title        = db.Column(db.String(200), nullable=False)
    author       = db.Column(db.String(100), nullable=False)
    genre        = db.Column(db.String(50))
    publish_year = db.Column(db.SmallInteger)
    total_pages  = db.Column(db.SmallInteger)
    isbn         = db.Column(db.String(20))
    created_at   = db.Column(db.DateTime, default=datetime.now)

    reading_progress = db.relationship('ReadingProgress', backref='book', lazy=True)
    meetings         = db.relationship('Meeting', backref='book', lazy=True)
    reviews          = db.relationship('Review', backref='book', lazy=True)


class Club(db.Model):
    __tablename__ = 'clubs'

    club_id      = db.Column(db.Integer, primary_key=True)
    club_name    = db.Column(db.String(100), nullable=False)
    description  = db.Column(db.String(1000))
    city         = db.Column(db.String(80))
    founded_date = db.Column(db.Date, nullable=False)
    created_at   = db.Column(db.DateTime, default=datetime.now)

    memberships = db.relationship('Membership', backref='club', lazy=True)
    meetings    = db.relationship('Meeting', backref='club', lazy=True)


class Membership(db.Model):
    __tablename__ = 'memberships'

    membership_id = db.Column(db.Integer, primary_key=True)
    member_id     = db.Column(db.Integer, db.ForeignKey('members.member_id', ondelete='CASCADE'), nullable=False)
    club_id       = db.Column(db.Integer, db.ForeignKey('clubs.club_id', ondelete='CASCADE'), nullable=False)
    role          = db.Column(db.String(30), default='member')
    created_at    = db.Column(db.DateTime, default=datetime.now)


class ReadingProgress(db.Model):
    __tablename__ = 'reading_progress'

    progress_id           = db.Column(db.Integer, primary_key=True)
    member_id             = db.Column(db.Integer, db.ForeignKey('members.member_id', ondelete='CASCADE'), nullable=False)
    book_id               = db.Column(db.Integer, db.ForeignKey('books.book_id', ondelete='CASCADE'), nullable=False)
    pages_read            = db.Column(db.SmallInteger, default=0)
    status                = db.Column(db.String(20), default='not_started')
    started_date          = db.Column(db.Date)
    finished_date         = db.Column(db.Date)
    last_updated          = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    completion_percentage = db.Column(db.Numeric(5, 2))


class Meeting(db.Model):
    __tablename__ = 'meetings'

    meeting_id   = db.Column(db.Integer, primary_key=True)
    club_id      = db.Column(db.Integer, db.ForeignKey('clubs.club_id', ondelete='CASCADE'), nullable=False)
    book_id      = db.Column(db.Integer, db.ForeignKey('books.book_id', ondelete='CASCADE'), nullable=False)
    meeting_date = db.Column(db.Date, nullable=False)
    location     = db.Column(db.String(150))
    notes        = db.Column(db.String(1000))
    created_at   = db.Column(db.DateTime, default=datetime.now)


class Review(db.Model):
    __tablename__ = 'reviews'

    review_id   = db.Column(db.Integer, primary_key=True)
    member_id   = db.Column(db.Integer, db.ForeignKey('members.member_id', ondelete='CASCADE'), nullable=False)
    book_id     = db.Column(db.Integer, db.ForeignKey('books.book_id', ondelete='CASCADE'), nullable=False)
    rating      = db.Column(db.SmallInteger, db.CheckConstraint('rating BETWEEN 1 AND 5'))
    review_text = db.Column(db.String(1000))
    created_at  = db.Column(db.DateTime, default=datetime.now)
