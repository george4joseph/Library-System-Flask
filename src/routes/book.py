import json
import math
from flask import Blueprint, jsonify, request
from src.controllers import book
import requests

bookRoutes = Blueprint('book_routes', __name__)

@bookRoutes.route('/view',methods=['GET'])
def view_book():
    name = request.args.get('name', default='', type=str)
    author = request.args.get('authors', default='', type=str)
    return book.getAllBooks(name,author)

@bookRoutes.route('view/<int:id>',methods=['GET'])
def viewSingleBook(id):
    return book.getBook(id)

@bookRoutes.route('edit/<int:id>',methods=['PATCH'])
def updateSingleBook(id):
    book_detail = json.loads(request.data)

    name = book_detail['name']
    author = book_detail['author']
    description = book_detail['description']
    base_fees = book_detail['base_fees']

    return book.updateBook(
        book_id=id,
        name=name,
        author=author,
        description=description,
        base_fees=base_fees
    )
@bookRoutes.route('delete/<int:id>',methods=['DELETE'])
def deleteSingleBook(id):
    return book.deleteBook(id)

@bookRoutes.route('import-books',methods=['GET'])
def importFromFrappe():
    count = request.args.get('count', default=1, type=int)
    title = request.args.get('name', default='', type=str)
    authors = request.args.get('authors', default='', type=str)
    
    page = 1  # Initialize page to 1
    pageMax = math.ceil(count / 20)
    bookCount = count
    savedBook = 0
    keepCount = 0
    print(page,pageMax)
    
    while page <= pageMax:
        # Construct the URL for the external API call with the current page value
        url = f"https://frappe.io/api/method/frappe-library?page={page}&title={title}&authors={authors}"
        
        # Make the external API call
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Assuming the response is JSON, parse it
            data = response.json()
            print(data)

            if len(data) == 0:
                break

            if bookCount <= 20:
                keepCount += book.processBooks(data['message'][:bookCount])
                savedBook += bookCount
                break
            else:
                keepCount += book.processBooks(data['message'])
                bookCount -= len(data)
                page += 1
                savedBook += len(data)

        else:
            return jsonify({'error': 'Invalid or missing book details'}), 400 
            break  # Break the loop in case of an error

    print(keepCount)
    result_data = {'message': 'Data imported successfully',
                   'imported_books': keepCount,
                   }
    return jsonify(result_data)


