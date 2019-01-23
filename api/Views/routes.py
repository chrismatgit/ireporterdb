from flask import Flask, jsonify, Blueprint
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from api.Utilities.validations import Incident_validation
from api.Controllers.user_controller import signup, admin_signup, login
from api.Controllers.incident_controller import create_incident, get_unique_red_flag, get_all_red_flags, update_red_flag_loc\
,update_red_flag_com, delete_red_flag, update_red_flag_status
from api.Controllers.intervention_controller import create_intervention, get_unique_intervention, get_all_interventions, \
update_intervention_loc
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

@bp.route('/red_flags/', methods=['GET'])
@jwt_required
def get_red_flags():
    response = get_all_red_flags()
    return response

@bp.route('/red_flags/<int:incident_id>/location', methods=['PATCH'])
@jwt_required
def update_red_flag_location(incident_id):
    response = update_red_flag_loc(incident_id)
    return response

@bp.route('/red_flags/<int:incident_id>/comment', methods=['PATCH'])
@jwt_required
def update_red_flag_comment(incident_id):
    response = update_red_flag_com(incident_id)
    return response

@bp.route('/red_flags/<int:incident_id>', methods=['DELETE'])
@jwt_required
def delete_a_unique_redflag(incident_id):
    response = delete_red_flag(incident_id)
    return response

@bp.route('/red_flags/<int:incident_id>/status', methods=['PATCH'])
@jwt_required
def update_red_flag_stat(incident_id):
    current_user=get_jwt_identity()
    user_data = db.query_one_user(current_user)
    if user_data['isadmin'] == False:
        return jsonify({
            "status": 401,
            "error": "Non admin user are not allowed"
        }) , 401 
    response = update_red_flag_status(incident_id)
    return response

####################interventions routes######################

@bp.route('/intervention/', methods=['POST'])
@jwt_required
def create_int():
    response = create_intervention()
    return response

@bp.route('/intervention/<int:intervention_id>', methods=['GET'])
@jwt_required
def get_intervention(intervention_id):
    response = get_unique_intervention(intervention_id)
    return response

@bp.route('/interventions/', methods=['GET'])
@jwt_required
def get_interventions():
    response = get_all_interventions()
    return response

@bp.route('/intervention/<int:intervention_id>/location', methods=['PATCH'])
@jwt_required
def update_interv_location(intervention_id):
    response = update_intervention_loc(intervention_id)
    return response
