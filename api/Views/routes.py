from flask import Flask, jsonify, Blueprint
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from api.Controllers.user_controller import signup, admin_signup
from db import DatabaseConnection

db = DatabaseConnection()
bp = Blueprint('application', __name__)

@bp.route('/')
def test_route():
    return "welcome to iReporter"

@bp.route('/signup/', methods=['POST'])
def signUp():
    response = signup()
    return response

@bp.route('/signup/admin', methods=['POST'])
def admin_user_signup():
    response = admin_signup()
    return response