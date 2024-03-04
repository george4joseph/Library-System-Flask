from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from db.main import load_config
from flask_migrate import Migrate



# Load the configuration for the specified environment

app = Flask(__name__)

config = load_config()

# Configure the PostgreSQL database URI
app.config['SQLALCHEMY_DATABASE_URI'] = config.get('DB', 'database_url')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = config.get('DB', 'api_key')

# Initialize the database with the Flask app
dbase = SQLAlchemy(app)
migrate = Migrate(app, dbase)


# Create an application context
with app.app_context():
    from db.model import User,Book
    # Create database tables if they do not exist
    dbase.create_all()
    print("Created the table")
    print(dbase.metadata)