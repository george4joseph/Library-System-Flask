from flask import Blueprint, Flask
from flask_sqlalchemy import SQLAlchemy
from db import app
from src.routes import member


# # Register the blueprint
app.register_blueprint(member.memberRoutes, url_prefix='/member')


