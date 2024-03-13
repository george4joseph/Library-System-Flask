import json
from flask import Blueprint, request
from src.controllers import member

memberRoutes = Blueprint('member_routes', __name__)

@memberRoutes.route('/view',methods=['GET'])
def view_member():
    return member.getAllMembers()

@memberRoutes.route('/view/<int:id>',methods=['GET'])
def viewSinglemember(id):
    return member.getMember(id)

@memberRoutes.route('/edit/<int:id>', methods=['PATCH'])
def editUser(id):
    user_details = json.loads(request.data)

    name = user_details.get('name')
    email = user_details.get('email')
    password = user_details.get('password')
    admin = user_details.get('admin')
    amount = user_details.get('amount')

    return member.updateUser(
        user_id=id,
        name=name,
        email=email,
        password=password,
        admin=admin,
        amount = amount
    )

@memberRoutes.route('/delete/<int:id>',methods=['DELETE'])
def deletemember(id):
    return member.deleteUser(id)

@memberRoutes.route('/create', methods=['POST'])
def createNewUser():
    user_details = json.loads(request.data)

    name = user_details.get('name')
    email = user_details.get('email')
    password = user_details.get('password')
    admin = user_details.get('admin')
    amount = user_details.get('amount')

    return member.createUser(
        name=name,
        email=email,
        password=password,
    )

# get_users_with_issued_books
@memberRoutes.route('/issued-books',methods=['GET'])
def booksIssued():
    return member.get_users_with_issued_books()