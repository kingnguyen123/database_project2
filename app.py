from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Member, Book, Club, Membership, ReadingProgress, Meeting, Review
from datetime import datetime, date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookclub.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'bookclubsecretkey123'

db.init_app(app)

with app.app_context():
    db.create_all()


# Dashboard 
@app.route('/')
def dashboard():
    total_members = Member.query.count()
    total_books   = Book.query.count()
    total_clubs   = Club.query.count()
    total_reviews = Review.query.count()

    avg_rating = db.session.query(db.func.avg(Review.rating)).scalar()
    avg_rating = round(avg_rating, 2) if avg_rating else 0

    completed   = ReadingProgress.query.filter_by(status='completed').count()
    in_progress = ReadingProgress.query.filter_by(status='in_progress').count()

    return render_template('dashboard.html',
        total_members=total_members,
        total_books=total_books,
        total_clubs=total_clubs,
        total_reviews=total_reviews,
        avg_rating=avg_rating,
        completed=completed,
        in_progress=in_progress
    )


# Members
@app.route('/members')
def members():
    all_members = Member.query.order_by(Member.last_name).all()
    return render_template('members.html', members=all_members)


@app.route('/members/add', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name  = request.form.get('last_name', '').strip()
        email      = request.form.get('email', '').strip()
        phone      = request.form.get('phone', '').strip()

        errors = []
        if not first_name:
            errors.append('First name is required')
        if not last_name:
            errors.append('Last name is required')
        if not email:
            errors.append('Email is required')
        elif Member.query.filter_by(email=email).first():
            errors.append('That email is already registered')

        if errors:
            for e in errors:
                flash(e, 'danger')
            return render_template('member_form.html', action='Add', member=None)

        member = Member(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone if phone else None,
            join_date=date.today()
        )
        db.session.add(member)
        db.session.commit()
        flash('Member added successfully!', 'success')
        return redirect(url_for('members'))

    return render_template('member_form.html', action='Add', member=None)


@app.route('/members/<int:member_id>/edit', methods=['GET', 'POST'])
def edit_member(member_id):
    member = Member.query.get_or_404(member_id)

    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name  = request.form.get('last_name', '').strip()
        email      = request.form.get('email', '').strip()
        phone      = request.form.get('phone', '').strip()

        errors = []
        if not first_name:
            errors.append('First name is required')
        if not last_name:
            errors.append('Last name is required')
        if not email:
            errors.append('Email is required')
        else:
            existing = Member.query.filter_by(email=email).first()
            if existing and existing.member_id != member_id:
                errors.append('That email is already registered to another member')

        if errors:
            for e in errors:
                flash(e, 'danger')
            return render_template('member_form.html', action='Edit', member=member)

        member.first_name = first_name
        member.last_name  = last_name
        member.email      = email
        member.phone      = phone if phone else None
        db.session.commit()
        flash('Member updated!', 'success')
        return redirect(url_for('members'))

    return render_template('member_form.html', action='Edit', member=member)


@app.route('/members/<int:member_id>/delete', methods=['POST'])
def delete_member(member_id):
    member = Member.query.get_or_404(member_id)
    db.session.delete(member)
    db.session.commit()
    flash('Member deleted', 'success')
    return redirect(url_for('members'))


#Books
@app.route('/books')
def books():
    all_books = Book.query.order_by(Book.title).all()
    return render_template('books.html', books=all_books)


@app.route('/books/<int:book_id>')
def book_detail(book_id):
    book    = Book.query.get_or_404(book_id)
    reviews = Review.query.filter_by(book_id=book_id).all()
    return render_template('book_detail.html', book=book, reviews=reviews)


@app.route('/books/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title        = request.form.get('title', '').strip()
        author       = request.form.get('author', '').strip()
        genre        = request.form.get('genre', '').strip()
        publish_year = request.form.get('publish_year', '').strip()
        total_pages  = request.form.get('total_pages', '').strip()
        isbn         = request.form.get('isbn', '').strip()

        errors = []
        if not title:
            errors.append('Title is required')
        if not author:
            errors.append('Author is required')
        if publish_year:
            try:
                publish_year = int(publish_year)
                if publish_year < 1000 or publish_year > date.today().year:
                    errors.append('Publish year must be a valid year')
            except ValueError:
                errors.append('Publish year must be a number')
        else:
            publish_year = None
        if total_pages:
            try:
                total_pages = int(total_pages)
                if total_pages < 1:
                    errors.append('Total pages must be at least 1')
            except ValueError:
                errors.append('Total pages must be a number')
        else:
            total_pages = None

        if errors:
            for e in errors:
                flash(e, 'danger')
            return render_template('book_form.html', action='Add', book=None)

        book = Book(
            title=title,
            author=author,
            genre=genre if genre else None,
            publish_year=publish_year,
            total_pages=total_pages,
            isbn=isbn if isbn else None
        )
        db.session.add(book)
        db.session.commit()
        flash('Book added successfully!', 'success')
        return redirect(url_for('books'))

    return render_template('book_form.html', action='Add', book=None)


@app.route('/books/<int:book_id>/edit', methods=['GET', 'POST'])
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)

    if request.method == 'POST':
        title        = request.form.get('title', '').strip()
        author       = request.form.get('author', '').strip()
        genre        = request.form.get('genre', '').strip()
        publish_year = request.form.get('publish_year', '').strip()
        total_pages  = request.form.get('total_pages', '').strip()
        isbn         = request.form.get('isbn', '').strip()

        errors = []
        if not title:
            errors.append('Title is required')
        if not author:
            errors.append('Author is required')
        if publish_year:
            try:
                publish_year = int(publish_year)
                if publish_year < 1000 or publish_year > date.today().year:
                    errors.append('Publish year must be a valid year')
            except ValueError:
                errors.append('Publish year must be a number')
        else:
            publish_year = None
        if total_pages:
            try:
                total_pages = int(total_pages)
                if total_pages < 1:
                    errors.append('Total pages must be at least 1')
            except ValueError:
                errors.append('Total pages must be a number')
        else:
            total_pages = None

        if errors:
            for e in errors:
                flash(e, 'danger')
            return render_template('book_form.html', action='Edit', book=book)

        book.title        = title
        book.author       = author
        book.genre        = genre if genre else None
        book.publish_year = publish_year
        book.total_pages  = total_pages
        book.isbn         = isbn if isbn else None
        db.session.commit()
        flash('Book updated!', 'success')
        return redirect(url_for('books'))

    return render_template('book_form.html', action='Edit', book=book)


@app.route('/books/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted', 'success')
    return redirect(url_for('books'))


#Clubs
@app.route('/clubs')
def clubs():
    all_clubs = Club.query.order_by(Club.club_name).all()
    return render_template('clubs.html', clubs=all_clubs)


@app.route('/clubs/<int:club_id>')
def club_detail(club_id):
    club = Club.query.get_or_404(club_id)
    return render_template('club_detail.html', club=club)


@app.route('/clubs/add', methods=['GET', 'POST'])
def add_club():
    if request.method == 'POST':
        club_name    = request.form.get('club_name', '').strip()
        description  = request.form.get('description', '').strip()
        city         = request.form.get('city', '').strip()
        founded_date = request.form.get('founded_date', '').strip()

        errors = []
        if not club_name:
            errors.append('Club name is required')
        if not founded_date:
            errors.append('Founded date is required')
        else:
            try:
                founded_date = datetime.strptime(founded_date, '%Y-%m-%d').date()
            except ValueError:
                errors.append('Founded date must be a valid date')

        if errors:
            for e in errors:
                flash(e, 'danger')
            return render_template('club_form.html', action='Add', club=None)

        club = Club(
            club_name=club_name,
            description=description if description else None,
            city=city if city else None,
            founded_date=founded_date
        )
        db.session.add(club)
        db.session.commit()
        flash('Club added successfully!', 'success')
        return redirect(url_for('clubs'))

    return render_template('club_form.html', action='Add', club=None)


@app.route('/clubs/<int:club_id>/edit', methods=['GET', 'POST'])
def edit_club(club_id):
    club = Club.query.get_or_404(club_id)

    if request.method == 'POST':
        club_name    = request.form.get('club_name', '').strip()
        description  = request.form.get('description', '').strip()
        city         = request.form.get('city', '').strip()
        founded_date = request.form.get('founded_date', '').strip()

        errors = []
        if not club_name:
            errors.append('Club name is required')
        if not founded_date:
            errors.append('Founded date is required')
        else:
            try:
                founded_date = datetime.strptime(founded_date, '%Y-%m-%d').date()
            except ValueError:
                errors.append('Founded date must be a valid date')

        if errors:
            for e in errors:
                flash(e, 'danger')
            return render_template('club_form.html', action='Edit', club=club)

        club.club_name    = club_name
        club.description  = description if description else None
        club.city         = city if city else None
        club.founded_date = founded_date
        db.session.commit()
        flash('Club updated!', 'success')
        return redirect(url_for('clubs'))

    return render_template('club_form.html', action='Edit', club=club)


@app.route('/clubs/<int:club_id>/delete', methods=['POST'])
def delete_club(club_id):
    club = Club.query.get_or_404(club_id)
    db.session.delete(club)
    db.session.commit()
    flash('Club deleted', 'success')
    return redirect(url_for('clubs'))


#Memberships
@app.route('/memberships/join', methods=['GET', 'POST'])
def join_club():
    all_members = Member.query.order_by(Member.last_name).all()
    all_clubs   = Club.query.order_by(Club.club_name).all()

    if request.method == 'POST':
        member_id = request.form.get('member_id', '').strip()
        club_id   = request.form.get('club_id', '').strip()
        role      = request.form.get('role', 'member').strip()

        errors = []
        if not member_id:
            errors.append('Please select a member')
        if not club_id:
            errors.append('Please select a club')
        if not errors:
            already = Membership.query.filter_by(
                member_id=int(member_id), club_id=int(club_id)
            ).first()
            if already:
                errors.append('That member is already in that club')

        if errors:
            for e in errors:
                flash(e, 'danger')
            return render_template('join_form.html', members=all_members, clubs=all_clubs)

        membership = Membership(
            member_id=int(member_id),
            club_id=int(club_id),
            role=role
        )
        db.session.add(membership)
        db.session.commit()
        flash('Member added to club successfully!', 'success')
        return redirect(url_for('clubs'))

    return render_template('join_form.html', members=all_members, clubs=all_clubs)


@app.route('/memberships/<int:membership_id>/remove', methods=['POST'])
def remove_member(membership_id):
    membership = Membership.query.get_or_404(membership_id)
    club_id    = membership.club_id
    db.session.delete(membership)
    db.session.commit()
    flash('Member removed from club', 'success')
    return redirect(url_for('club_detail', club_id=club_id))


#Reading Progress
@app.route('/progress')
def progress():
    all_progress = ReadingProgress.query.order_by(ReadingProgress.last_updated.desc()).all()
    return render_template('progress.html', progress=all_progress)


@app.route('/progress/log', methods=['GET', 'POST'])
def log_progress():
    all_members = Member.query.order_by(Member.last_name).all()
    all_books   = Book.query.order_by(Book.title).all()

    if request.method == 'POST':
        member_id     = request.form.get('member_id', '').strip()
        book_id       = request.form.get('book_id', '').strip()
        pages_read    = request.form.get('pages_read', '0').strip()
        status        = request.form.get('status', 'not_started').strip()
        started_date  = request.form.get('started_date', '').strip()
        finished_date = request.form.get('finished_date', '').strip()

        errors = []
        if not member_id:
            errors.append('Please select a member')
        if not book_id:
            errors.append('Please select a book')
        try:
            pages_read = int(pages_read)
            if pages_read < 0:
                errors.append('Pages read cannot be negative')
        except ValueError:
            errors.append('Pages read must be a number')

        if errors:
            for e in errors:
                flash(e, 'danger')
            return render_template('progress_form.html', members=all_members, books=all_books)

        book = Book.query.get(int(book_id))

       
        if book.total_pages and book.total_pages > 0:
            completion = round((pages_read / book.total_pages) * 100, 2)
        else:
            completion = None

        progress = ReadingProgress.query.filter_by(
            member_id=int(member_id), book_id=int(book_id)
        ).first()

        if progress:
            progress.pages_read            = pages_read
            progress.status                = status
            progress.completion_percentage = completion
            progress.last_updated          = datetime.now()
            progress.started_date  = datetime.strptime(started_date, '%Y-%m-%d').date() if started_date else progress.started_date
            progress.finished_date = datetime.strptime(finished_date, '%Y-%m-%d').date() if finished_date else None
        else:
            progress = ReadingProgress(
                member_id=int(member_id),
                book_id=int(book_id),
                pages_read=pages_read,
                status=status,
                completion_percentage=completion,
                started_date=datetime.strptime(started_date, '%Y-%m-%d').date() if started_date else None,
                finished_date=datetime.strptime(finished_date, '%Y-%m-%d').date() if finished_date else None
            )
            db.session.add(progress)

        db.session.commit()
        flash('Reading progress saved!', 'success')
        return redirect(url_for('progress'))

    return render_template('progress_form.html', members=all_members, books=all_books)


#Reviews
@app.route('/reviews')
def reviews():
    all_reviews = Review.query.order_by(Review.created_at.desc()).all()
    return render_template('reviews.html', reviews=all_reviews)


@app.route('/reviews/add', methods=['GET', 'POST'])
def add_review():
    all_members = Member.query.order_by(Member.last_name).all()
    all_books   = Book.query.order_by(Book.title).all()

    if request.method == 'POST':
        member_id   = request.form.get('member_id', '').strip()
        book_id     = request.form.get('book_id', '').strip()
        rating      = request.form.get('rating', '').strip()
        review_text = request.form.get('review_text', '').strip()

        errors = []
        if not member_id:
            errors.append('Please select a member')
        if not book_id:
            errors.append('Please select a book')
        if not rating:
            errors.append('Rating is required')
        else:
            try:
                rating = int(rating)
                if rating < 1 or rating > 5:
                    errors.append('Rating must be between 1 and 5')
            except ValueError:
                errors.append('Rating must be a number')

        if errors:
            for e in errors:
                flash(e, 'danger')
            return render_template('review_form.html', members=all_members, books=all_books)

        review = Review(
            member_id=int(member_id),
            book_id=int(book_id),
            rating=rating,
            review_text=review_text if review_text else None
        )
        db.session.add(review)
        db.session.commit()
        flash('Review added!', 'success')
        return redirect(url_for('reviews'))

    return render_template('review_form.html', members=all_members, books=all_books)


@app.route('/reviews/<int:review_id>/delete', methods=['POST'])
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    db.session.delete(review)
    db.session.commit()
    flash('Review deleted', 'success')
    return redirect(url_for('reviews'))


#Meetings
@app.route('/meetings')
def meetings():
    all_meetings = Meeting.query.order_by(Meeting.meeting_date.desc()).all()
    return render_template('meetings.html', meetings=all_meetings)


@app.route('/meetings/add', methods=['GET', 'POST'])
def add_meeting():
    all_clubs = Club.query.order_by(Club.club_name).all()
    all_books = Book.query.order_by(Book.title).all()

    if request.method == 'POST':
        club_id      = request.form.get('club_id', '').strip()
        book_id      = request.form.get('book_id', '').strip()
        meeting_date = request.form.get('meeting_date', '').strip()
        location     = request.form.get('location', '').strip()
        notes        = request.form.get('notes', '').strip()

        errors = []
        if not club_id:
            errors.append('Please select a club')
        if not book_id:
            errors.append('Please select a book')
        if not meeting_date:
            errors.append('Meeting date is required')
        else:
            try:
                meeting_date = datetime.strptime(meeting_date, '%Y-%m-%d').date()
            except ValueError:
                errors.append('Meeting date must be a valid date')

        if errors:
            for e in errors:
                flash(e, 'danger')
            return render_template('meeting_form.html', clubs=all_clubs, books=all_books)

        meeting = Meeting(
            club_id=int(club_id),
            book_id=int(book_id),
            meeting_date=meeting_date,
            location=location if location else None,
            notes=notes if notes else None
        )
        db.session.add(meeting)
        db.session.commit()
        flash('Meeting added!', 'success')
        return redirect(url_for('meetings'))

    return render_template('meeting_form.html', clubs=all_clubs, books=all_books)


@app.route('/meetings/<int:meeting_id>/delete', methods=['POST'])
def delete_meeting(meeting_id):
    meeting = Meeting.query.get_or_404(meeting_id)
    db.session.delete(meeting)
    db.session.commit()
    flash('Meeting deleted', 'success')
    return redirect(url_for('meetings'))


if __name__ == '__main__':
    app.run(debug=True)
