from db.model import Book, IssueBook,User
from db import dbase as db
from flask import flash, jsonify

def getAllMembers():
    users = User.query.all()
    dataJson = [user.to_dict() for user in users]
    return jsonify(status=200, data=dataJson),200
    

def getMember(id):
    user = User.query.get_or_404(id)
    return jsonify(status=200, data=user.to_dict())

def updateUser(user_id, name, email, password, admin, amount):
    user = User.query.get(user_id)
    if name:
        user.name = name
    if email:
        user.email = email
    if password:
        user.password = password
    if admin is not None:
        user.admin = admin
    if amount is not None:
        user.amount = amount

    
    db.session.add(user)
    db.session.commit()
    user = User.query.get(user_id)
    return jsonify(status=200, data= user.to_dict())

def deleteUser(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200

def createUser(name, email, password, admin=False):
    # Create a new user instance
    new_user = User(name=name, email=email, password=password, admin=admin)

    # Add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    # Return the details of the created user as a JSON response
    return jsonify(new_user.to_dict())

def get_users_with_issued_books():
    users_with_books = []

    # Fetch all users
    users = User.query.all()

    for user in users:
        user_dict = user.to_dict()
        issued_books = []

        # Fetch issued books for the current user
        issued_books_query = IssueBook.query.filter_by(issued_by=user.id).all()

        for issued_book in issued_books_query:
            issued_books.append(issued_book.to_dict())

        # Add the list of issued books to the user dictionary
        user_dict['issued_books'] = issued_books
        users_with_books.append(user_dict)

    return jsonify(users_with_books)