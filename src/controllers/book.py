from db.model import Book
from db import dbase
from flask import flash,jsonify, request

def getAllBooks(name,author):
    # Query all books
    query = Book.query

    # Apply filters if provided
    if name:
        query = query.filter(Book.name.ilike(f'%{name}%'))
    if author:
        query = query.filter(Book.author.ilike(f'%{author}%'))

    # Execute the query and return the results as JSON
    books = query.all()
    return jsonify([book.to_dict() for book in books])
    
def getBook(id):
    books = Book.query.get_or_404(id)
    return jsonify(books.to_dict())

def updateBook(book_id, name, author, description, base_fees):
    book = Book.query.get(book_id)
    book.name = name
    book.author = author
    book.description = description
    book.base_fees = base_fees

    dbase.session.add(book)
    dbase.session.commit()

    return jsonify(book.to_dict())

def deleteBook(id):
    book = Book.query.get_or_404(id)
    dbase.session.delete(book)
    dbase.session.commit()
    return jsonify({'message': 'Book deleted'}), 204

def createBook(name, author, description, base_fees):
    
    # Create a new book instance
    new_book = Book(name=name, author=author, description=description, base_fees=base_fees)

    # Add the new book to the database
    dbase.session.add(new_book)
    dbase.session.commit()

    # Return the details of the created book as a JSON response
    return jsonify(new_book.to_dict())

def processBooks(bookDetails):
    savedCount = 0
    for bookDetail in bookDetails:
        # Check if a book with the same name already exists
        existing_book = Book.query.filter_by(name=bookDetail['title']).first()
        if existing_book:
            continue  

        createBook(bookDetail['title'], bookDetail['authors'], '', 50)
        savedCount += 1
    return savedCount
