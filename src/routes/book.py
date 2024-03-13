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

@bookRoutes.route('create',methods=['POST'])
def createSingleBook():
    name, author, description, base_fees
    book_detail = json.loads(request.data)
    name = book_detail.get('name')
    author = book_detail.get('author')
    description = book_detail.get('description')
    base_fees = book_detail.get('base_fees')
    total_copy = book_detail.get('total_copy')
    return book.createBook()

# issue_book
@bookRoutes.route('issue',methods=['POST'])
def issueSingleBook():
    book_detail = json.loads(request.data)
    issued_by = book_detail.get('user_id')
    book_id = book_detail.get('book_id')
    date_issued = book_detail.get('date')
    return book.issue_book(issued_by,book_id,date_issued)

@bookRoutes.route('return',methods=['POST'])
def returnSingleBook():
    book_detail = json.loads(request.data)
    issue_id = book_detail.get('issue_id')
    amount_paid = book_detail.get('amount_paid')
    date_return = book_detail.get('date_return')
    return book.return_book(amount_paid=amount_paid, date_return=date_return, issue_id=issue_id)

@bookRoutes.route('edit/<int:id>',methods=['PATCH'])
def updateSingleBook(id):
    book_detail = json.loads(request.data)
    name = book_detail.get('name')
    author = book_detail.get('author')
    description = book_detail.get('description')
    base_fees = book_detail.get('base_fees')
    total_copy = book_detail.get('total_copy')
    issued_copy = book_detail.get('issued_copy')
    present_copy = book_detail.get('present_copy')

    return book.updateBook(
        book_id=id,
        name=name,
        author=author,
        description=description,
        base_fees=base_fees,
        total_copy=total_copy,
        issued_copy=issued_copy,
        present_copy=present_copy,

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
                   'status': 200,
                   'imported_books': keepCount,
                   }
    return jsonify(result_data)


