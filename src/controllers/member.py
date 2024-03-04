from db.model import Book,User
from db import dbase
from flask import flash

def getMember():
    # user = Book.query.all()
    book = Book(
            name="name",
            author="author",
            description="description",
            total_copy=4,
            present_copy=4,
            issued_copy=0,
    )
    dbase.session.add(book)
    user = User(
        name="Geo",
        email="wer@",
        password="1234rty",
        admin=False
    )
    dbase.session.add(user)
    dbase.session.commit()
    flash("Book added successfully!")
    # print("Memeber are we")
    return "Good"