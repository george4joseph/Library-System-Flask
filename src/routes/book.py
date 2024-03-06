from flask import Blueprint
from src.controllers import book

bookRoutes = Blueprint('book_routes', __name__)

@bookRoutes.route('/view',methods=['GET'])
def view_book():
    return book.getAllBooks()

@bookRoutes.route('view/<int:id>')
def viewSingleBook(id):
    return book.getBook(id)

