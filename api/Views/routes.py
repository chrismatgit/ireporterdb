from flask import Flask, jsonify, Blueprint
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from api.Controllers.user_controller import signup, admin_signup, login
from api.Controllers.incident_controller import create_incident, get_unique_red_flag
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

@bp.route('/login/', methods=['POST']) 
def user_login():
    response = login()
    return response

@bp.route('/red_flag/', methods=['POST'])
@jwt_required
def create_report():
    response = create_incident()
    return response

@bp.route('/red_flag/<int:incident_id>', methods=['GET'])
@jwt_required
def get_red_flag(incident_id):
    response = get_unique_red_flag(incident_id)
    return response
