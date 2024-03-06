
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from db import dbase as db


class User(UserMixin,db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    book = db.relationship("IssueBook", backref="issue", lazy=True)
    admin = db.Column(db.Boolean, default=False)


class IssueBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(db.DateTime())
    issued_by = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=True, default=None
    )
    date_issued = db.Column(db.DateTime(), default=None)
    date_return = db.Column(db.DateTime(), default=None)
    book = db.Column(db.Integer, db.ForeignKey("book.id"))

class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    author = db.Column(db.String(255))
    description = db.Column(db.Text)
    total_copy = db.Column(db.Integer)
    issued_copy = db.Column(db.Integer)
    present_copy = db.Column(db.Integer)
    base_fees = db.Column(db.Integer)
    issue = db.relationship(
        "IssueBook", backref=db.backref("posts", lazy=True), cascade="all,delete"
    )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'author': self.author,
            'description': self.description,
            'total_copy': self.total_copy,
            'issued_copy': self.issued_copy,
            'present_copy': self.present_copy,
            # Exclude the 'issue' relationship to avoid circular serialization
        }

# class Book(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255), unique=True)
#     author = db.Column(db.String(255))
#     description = db.Column(db.Text)
#     copy = db.relationship(
#         "Copy", backref=db.backref("posts", lazy=True), cascade="all,delete"
#     )
#     total_copy = db.Column(db.Integer)
#     issued_copy = db.Column(db.Integer)
#     present_copy = db.Column(db.Integer)