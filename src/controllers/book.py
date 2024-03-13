from datetime import datetime
from db.model import Book, IssueBook, User
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
    bookJson = [book.to_dict() for book in books]
    return jsonify(status = 200, data = bookJson)
    
def getBook(id):
    books = Book.query.get_or_404(id)
    return jsonify(status = 200, data = books.to_dict())
    # return jsonify(books.to_dict())

def updateBook(book_id, name, author, description, base_fees, total_copy, issued_copy, present_copy):
    book = Book.query.get(book_id)
    if name:
        book.name = name
    if author:
        book.author = author
    if description:
        book.description = description
    if base_fees is not None:
        book.base_fees = base_fees
    if total_copy is not None:
        book.total_copy = total_copy
    if issued_copy is not None:
        book.issued_copy = issued_copy
    if present_copy is not None:
        book.present_copy = present_copy

    dbase.session.add(book)
    dbase.session.commit()

    return jsonify(status = 200, data = book.to_dict()), 200

def deleteBook(id):
    book = Book.query.get(id)
    dbase.session.delete(book)
    dbase.session.commit()
    return jsonify({'message': 'Book deleted', "status": 200}), 200

def createBook(name, author, description, base_fees):
    
    # Create a new book instance
    new_book = Book(name=name, author=author, description=description, base_fees=base_fees, total_copy = 10, present_copy = 10, issued_copy = 0)

    # Add the new book to the database
    dbase.session.add(new_book)
    dbase.session.commit()

    # Return the details of the created book as a JSON response
    return jsonify(status = 200, data = new_book.to_dict())

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


# issue the books
def issue_book(issued_by, book_id, date_issued):
    # Create a new instance of IssueBook
    books = Book.query.get_or_404(book_id)
    issue = IssueBook(
        issued_by=issued_by,
        book=book_id,
        date_issued=datetime.strptime(date_issued, "%d-%m-%Y"),
        amount= books.base_fees
    )
    # updateBook(issued_copy=1, present_copy= books.total_copy - books.issued_copy - 1)
    books.issued_copy += 1 
    books.present_copy = books.total_copy - books.issued_copy 

    user = User.query.get(issued_by)
    user.amount_pending = user.amount_pending + books.base_fees

    if user.amount_pending >= 500:
        return jsonify({'message': 'You have pending Rs 500'}), 400
    # updateUser(user_id=issued_by,amount=user.amount + books.base_fees)

    # Save the instance to the database
    dbase.session.add(issue)
    dbase.session.add(books)
    dbase.session.add(user)

    
    dbase.session.commit()
    # Return the details of the created book as a JSON response
    return jsonify(issue.to_dict())

# issue the books
def return_book(issue_id, date_return, amount_paid):
    # Create a new instance of IssueBook
    issue = IssueBook.query.get_or_404(issue_id)
    issue.date_return = datetime.strptime(date_return, "%d-%m-%Y")
    issue.amount_paid = amount_paid
    
    books = Book.query.get_or_404(issue.book)
    books.issued_copy = books.issued_copy - 1 
    books.present_copy = books.present_copy + 1

    if amount_paid:
        user = User.query.get(issue.issued_by)
        user.amount_pending = user.amount_pending - amount_paid
        dbase.session.add(user)

    # Save the instance to the database
    dbase.session.add(issue)
    dbase.session.add(books)
    
    dbase.session.commit()

    issue = IssueBook.query.get_or_404(issue_id)
    # Return the details of the created book as a JSON response
    return jsonify(status = 200, data = issue.to_dict()), 200