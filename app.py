from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Author, Book, Member, Loan
from datetime import date, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'librarysecretkey123'

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def dashboard():
    return render_template('dashboard.html')


@app.route('/authors')
def authors():
    all_authors = Author.query.order_by(Author.last_name).all()
    return render_template('authors.html', authors=all_authors)


@app.route('/authors/add', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        birth_year = request.form.get('birth_year', '').strip()

        errors = []
        if not first_name:
            errors.append('First name is required')
        if not last_name:
            errors.append('Last name is required')
        if birth_year:
            try:
                birth_year = int(birth_year)
                if birth_year < 1000 or birth_year > date.today().year:
                    errors.append('Birth year must be a valid year')
            except ValueError:
                errors.append('Birth year must be a number')
        else:
            birth_year = None

        if errors:
            for e in errors:
                flash(e, 'danger')
            return render_template('author_form.html', action='Add', author=None)

        author = Author(first_name=first_name, last_name=last_name, birth_year=birth_year)
        db.session.add(author)
        db.session.commit()
        flash('Author added successfully!', 'success')
        return redirect(url_for('authors'))

    return render_template('author_form.html', action='Add', author=None)


@app.route('/authors/<int:author_id>/edit', methods=['GET', 'POST'])
def edit_author(author_id):
    author = Author.query.get_or_404(author_id)

    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        birth_year = request.form.get('birth_year', '').strip()

        errors = []
        if not first_name:
            errors.append('First name is required')
        if not last_name:
            errors.append('Last name is required')
        if birth_year:
            try:
                birth_year = int(birth_year)
                if birth_year < 1000 or birth_year > date.today().year:
                    errors.append('Birth year must be a valid year')
            except ValueError:
                errors.append('Birth year must be a number')
        else:
            birth_year = None

        if errors:
            for e in errors:
                flash(e, 'danger')
            return render_template('author_form.html', action='Edit', author=author)

        author.first_name = first_name
        author.last_name = last_name
        author.birth_year = birth_year
        db.session.commit()
        flash('Author updated!', 'success')
        return redirect(url_for('authors'))

    return render_template('author_form.html', action='Edit', author=author)


@app.route('/authors/<int:author_id>/delete', methods=['POST'])
def delete_author(author_id):
    author = Author.query.get_or_404(author_id)
    if author.books:
        flash('Cannot delete an author who has books in the system', 'danger')
        return redirect(url_for('authors'))
    db.session.delete(author)
    db.session.commit()
    flash('Author deleted', 'success')
    return redirect(url_for('authors'))


@app.route('/books')
def books():
    all_books = Book.query.join(Author).order_by(Book.title).all()
    return render_template('books.html', books=all_books)


@app.route('/books/<int:book_id>')
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book_detail.html', book=book)


@app.route('/books/add', methods=['GET', 'POST'])
def add_book():
    all_authors = Author.query.order_by(Author.last_name).all()

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        author_id = request.form.get('author_id', '').strip()
        genre = request.form.get('genre', '').strip()
        total_copies = request.form.get('total_copies', '').strip()
        price = request.form.get('price', '').strip()

        errors = []
        if not title:
            errors.append('Title is required')
        if not author_id:
            errors.append('Please select an author')
        if not total_copies:
            errors.append('Total copies is required')
        else:
            try:
                total_copies = int(total_copies)
                if total_copies < 1:
                    errors.append('Total copies must be at least 1')
            except ValueError:
                errors.append('Total copies must be a whole number')
        if not price:
            errors.append('Price is required')
        else:
            try:
                price = float(price)
                if price < 0:
                    errors.append('Price cannot be negative')
            except ValueError:
                errors.append('Price must be a number')

        if errors:
            for e in errors:
                flash(e, 'danger')
            return render_template('book_form.html', action='Add', book=None, authors=all_authors)

        book = Book(
            title=title,
            author_id=int(author_id),
            genre=genre if genre else None,
            total_copies=total_copies,
            available_copies=total_copies,
            price=price
        )
        db.session.add(book)
        db.session.commit()
        flash('Book added successfully!', 'success')
        return redirect(url_for('books'))

    return render_template('book_form.html', action='Add', book=None, authors=all_authors)


@app.route('/books/<int:book_id>/edit', methods=['GET', 'POST'])
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    all_authors = Author.query.order_by(Author.last_name).all()

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        author_id = request.form.get('author_id', '').strip()
        genre = request.form.get('genre', '').strip()
        total_copies = request.form.get('total_copies', '').strip()
        price = request.form.get('price', '').strip()

        loaned_out = book.total_copies - book.available_copies

        errors = []
        if not title:
            errors.append('Title is required')
        if not author_id:
            errors.append('Please select an author')
        if not total_copies:
            errors.append('Total copies is required')
        else:
            try:
                total_copies = int(total_copies)
                if total_copies < 1:
                    errors.append('Total copies must be at least 1')
                elif total_copies < loaned_out:
                    errors.append(f'Cannot set total copies below {loaned_out} (currently checked out)')
            except ValueError:
                errors.append('Total copies must be a whole number')
        if not price:
            errors.append('Price is required')
        else:
            try:
                price = float(price)
                if price < 0:
                    errors.append('Price cannot be negative')
            except ValueError:
                errors.append('Price must be a number')

        if errors:
            for e in errors:
                flash(e, 'danger')
            return render_template('book_form.html', action='Edit', book=book, authors=all_authors)

        book.title = title
        book.author_id = int(author_id)
        book.genre = genre if genre else None
        book.available_copies = total_copies - loaned_out
        book.total_copies = total_copies
        book.price = price
        db.session.commit()
        flash('Book updated!', 'success')
        return redirect(url_for('books'))

    return render_template('book_form.html', action='Edit', book=book, authors=all_authors)


@app.route('/members')
def members():
    all_members = Member.query.order_by(Member.last_name).all()
    return render_template('members.html', members=all_members)


@app.route('/members/add', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()

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
            phone=phone if phone else None
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
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()

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
        member.last_name = last_name
        member.email = email
        member.phone = phone if phone else None
        db.session.commit()
        flash('Member updated!', 'success')
        return redirect(url_for('members'))

    return render_template('member_form.html', action='Edit', member=member)


@app.route('/members/<int:member_id>/delete', methods=['POST'])
def delete_member(member_id):
    member = Member.query.get_or_404(member_id)
    if member.loans:
        flash('Cannot delete a member who has loan records', 'danger')
        return redirect(url_for('members'))
    db.session.delete(member)
    db.session.commit()
    flash('Member deleted', 'success')
    return redirect(url_for('members'))


@app.route('/loans')
def loans():
    all_loans = Loan.query.order_by(Loan.loan_date.desc()).all()
    return render_template('loans.html', loans=all_loans, today=date.today())


@app.route('/loans/checkout', methods=['GET', 'POST'])
def checkout():
    all_members = Member.query.order_by(Member.last_name).all()
    available_books = Book.query.filter(Book.available_copies > 0).order_by(Book.title).all()

    if request.method == 'POST':
        member_id = request.form.get('member_id', '').strip()
        book_id = request.form.get('book_id', '').strip()

        errors = []
        if not member_id:
            errors.append('Please select a member')
        if not book_id:
            errors.append('Please select a book')

        if not errors:
            book = Book.query.get(int(book_id))
            if book.available_copies < 1:
                errors.append('That book has no available copies')

        if errors:
            for e in errors:
                flash(e, 'danger')
            return render_template('checkout_form.html', members=all_members, books=available_books)

        loan = Loan(
            book_id=int(book_id),
            member_id=int(member_id),
            loan_date=date.today(),
            due_date=date.today() + timedelta(days=14),
            status='active'
        )
        db.session.add(loan)
        book.available_copies -= 1
        db.session.commit()

        flash('Book checked out successfully!', 'success')
        return redirect(url_for('loans'))

    return render_template('checkout_form.html', members=all_members, books=available_books)


@app.route('/books/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.total_copies != book.available_copies:
        flash('Cannot delete a book that has copies currently checked out', 'danger')
        return redirect(url_for('books'))
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted', 'success')
    return redirect(url_for('books'))


if __name__ == '__main__':
    app.run(debug=True)
