from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Book, Borrow
from . import db
from .qr_utils import generate_qr
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

@main.route('/add-book', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    qr_data = f"{title}|{author}"
    qr_path = generate_qr(qr_data)

    new_book = Book(title=title, author=author, qr_code=qr_path)
    db.session.add(new_book)
    db.session.commit()
    return redirect(url_for('main.index'))

@main.route('/scan', methods=['GET', 'POST'])
def scan():
    if request.method == 'POST':
        qr_data = request.form['qr_data']
        student_id = request.form['student_id']

        try:
            title, author = qr_data.split('|')
        except:
            flash('QR format xato!')
            return redirect(url_for('main.scan'))

        book = Book.query.filter_by(title=title.strip(), author=author.strip()).first()

        if book and not book.is_borrowed:
            book.is_borrowed = True
            borrow = Borrow(student_id=student_id, book_id=book.id)
            db.session.add(borrow)
            db.session.commit()
            flash('Kitob muvaffaqiyatli berildi!')

        elif book and book.is_borrowed:
            borrow = Borrow.query.filter_by(book_id=book.id, student_id=student_id, return_date=None).order_by(Borrow.id.desc()).first()
            if borrow:
                borrow.return_date = datetime.utcnow()
                db.session.delete(borrow)
                book.is_borrowed = False
                db.session.commit()
                flash('Kitob qaytarildi va borrowdan o‘chirildi!')
            else:
                flash('Talaba tomonidan olingan kitob topilmadi.')
        else:
            flash('Kitob topilmadi')

        return redirect(url_for('main.scan'))

    return render_template('scan.html')

@main.route('/admin')
def admin():
    borrows = Borrow.query.order_by(Borrow.borrow_date.desc()).all()
    return render_template('admin.html', borrows=borrows)