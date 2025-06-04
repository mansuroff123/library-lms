from . import db
from datetime import datetime

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    author = db.Column(db.String(100))
    qr_code = db.Column(db.String(300))
    is_borrowed = db.Column(db.Boolean, default=False)

class Borrow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    borrow_date = db.Column(db.DateTime, default=datetime.utcnow)
    return_date = db.Column(db.DateTime, nullable=True)