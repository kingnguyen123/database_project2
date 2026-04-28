from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Author
from datetime import date

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
            errors.append('First name is required.')
        if not last_name:
            errors.append('Last name is required.')
        if birth_year:
            try:
                birth_year = int(birth_year)
                if birth_year < 1000 or birth_year > date.today().year:
                    errors.append('Birth year must be a valid year.')
            except ValueError:
                errors.append('Birth year must be a number.')
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
            errors.append('First name is required.')
        if not last_name:
            errors.append('Last name is required.')
        if birth_year:
            try:
                birth_year = int(birth_year)
                if birth_year < 1000 or birth_year > date.today().year:
                    errors.append('Birth year must be a valid year.')
            except ValueError:
                errors.append('Birth year must be a number.')
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
        flash('Cannot delete an author who has books in the system.', 'danger')
        return redirect(url_for('authors'))
    db.session.delete(author)
    db.session.commit()
    flash('Author deleted.', 'success')
    return redirect(url_for('authors'))


if __name__ == '__main__':
    app.run(debug=True)
