from flask import Flask, jsonify, request
from db import DatabaseConnection
from api.Models.Intervention import Intervention
from api.Utilities.validations import Incident_validation
from flask_jwt_extended import get_jwt_identity
import datetime

db = DatabaseConnection()

def create_intervention():
    '''Function creates a new intervention to the database
    :returns:
    a success message and the intervention.
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
        invalid_status = validator.validate_intervention_type(inctype)
        if invalid_status:
            return jsonify(invalid_status), 400 
        if invalid_data:
            return jsonify(invalid_data), 400

        new_intervention = db.insert_intervention(createdon, createdby, inctype, location, status, image, video, comment)
        return jsonify({
            "status": 201,
            "data": new_intervention,
            "message": f"{inctype} has been created successfuly"
        }), 201

    except Exception:
        return jsonify({
            'status': 400,
            'error': 'Something went wrong with your inputs'
        }), 400
