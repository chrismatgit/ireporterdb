
from flask import Flask, jsonify, request
from db import DatabaseConnection
from api.Models.Incidents import Incident
from api.Utilities.validations import Incident_validation
# from flask_jwt_extended import get_jwt_identity
import datetime

db = DatabaseConnection()

def create_incident():
    '''Function creates a new incident to the database
    :returns:
    a success message and the incident.
    '''
    try:
        # current_user = get_jwt_identity()
        data = request.get_json()
        #incident_id = len(Incident.reports)+1
        createdon = datetime.datetime.now()
        # createdby = current_user
        createdby = data.get("createdby")
        inctype = data.get("inctype")
        location = data.get("location")
        status = "delivered"
        image = data.get("image")
        video = data.get("video")
        comment = data.get("comment")

        # validation
        validator = Incident_validation()
        invalid_data = validator.add_incident_validation(createdby,location,status,image,video,comment)
        invalid_status = validator.validate_red_flag_inctype(inctype)
        if invalid_status:
            return jsonify(invalid_status), 400
        if invalid_data:
            return jsonify(invalid_data), 400

        new_incident = db.insert_incident(createdon, createdby, inctype, location, status, image, video, comment)
        return jsonify({
            "status": 201,
            "data": new_incident,
            "message": f"{inctype} has been created successfuly"
        }), 201

    except Exception:
        return jsonify({
            'status': 400,
            'error': 'Something went wrong with your inputs'
        }), 400

def get_unique_red_flag(incident_id):
    ''' Function enables the user to update a single red-flag record
    :param:
    incident_id - holds integer value of the id of the individual red-flag 
    :returns:
    A success message and the Details of the red-flag whose id matches the one entered 
    '''
    validator = Incident_validation()
    no_data = validator.check_if_empty()
    not_exist = validator.check_if_red_flag_exist(incident_id)
    if no_data:
        return no_data 
    if not_exist: 
        return not_exist
    try:
        incident = db.query_one(incident_id)
        return jsonify({
            'status': 200,
            'data': incident,
            'message': 'Red-Flag Fetched'
            }), 200
    except Exception:
        return jsonify({
            'status': 400,
            'error': 'Something went wrong'
        }), 400

