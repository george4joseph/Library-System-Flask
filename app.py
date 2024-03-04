from flask import Blueprint, Flask
from flask_sqlalchemy import SQLAlchemy
from db import main
from src.routes import member


app = Flask(__name__)

# Load the configuration for the specified environment
config = main.load_config()

# Configure the PostgreSQL database URI
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://your_username:your_password@localhost/your_database'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = config.get('DB', 'database_url')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the Flask app
dbase = SQLAlchemy(app)

# member_routes_blueprint = Blueprint('member_routes', __name__, url_prefix='/member')

# # Register the Blueprint with the Flask application
# app.register_blueprint(member_routes_blueprint)

# # Register the blueprint
app.register_blueprint(member.memberRoutes, url_prefix='/member')

if __name__ == '__main__':
    # Create database tables if they do not exist
    dbase.create_all()
    app.run(debug=True)
