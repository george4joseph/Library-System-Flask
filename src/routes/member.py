from flask import Blueprint
from src.controllers import member

memberRoutes = Blueprint('member_routes', __name__)

@memberRoutes.route('/view',methods=['GET'])
def view_member():
    return member.getMember()

