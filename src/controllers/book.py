from db.model import Book
from db import dbase
from flask import flash,jsonify

def getAllBooks():
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books])
    
def getBook(id):
    books = Book.query.get_or_404(id)
    return jsonify(books.to_dict())

