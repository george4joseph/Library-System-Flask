from flask import Blueprint, Flask
from flask_sqlalchemy import SQLAlchemy
from db import app
from src.routes import member,book


# # Register the blueprint
app.register_blueprint(member.memberRoutes, url_prefix='/member')
app.register_blueprint(book.bookRoutes, url_prefix='/book')


