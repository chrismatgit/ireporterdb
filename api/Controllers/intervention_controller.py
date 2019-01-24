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

def get_unique_intervention(intervention_id):
    ''' Function enables the user to get a single intervention record
    :param:
    incident_id - holds integer value of the id of the individual red-flag 
    :returns:
    A success message and the Details of the red-flag whose id matches the one entered 
    '''
    validator = Incident_validation()
    no_data = validator.check_if_empty_intervention()
    not_exist = validator.check_if_intervention_exist(intervention_id)
    if no_data:
        return no_data 
    if not_exist: 
        return not_exist
    try:
        interv = db.query_one_intervention(intervention_id)
        return jsonify({
            'status': 200,
            'data': interv,
            'message': 'Intervention Fetched'
            }), 200
    except Exception:
        return jsonify({
            'status': 400,
            'error': 'Something went wrong'
        }), 400

def get_all_interventions():
    ''' Function enables the view of all the interventions
    :returns:
    A list of all the interventions created
    '''
    validator = Incident_validation()
    no_data = validator.check_if_empty_intervention()
    if no_data:
        return no_data 
    interventions = db.query_all("interventions")
    for intervention in interventions:
        intervention_dict = {
            "intervention_id": intervention["intervention_id"],
            "createdon": intervention["createdon"],
            "createdby": intervention["createdby"],
            "inctype": intervention["inctype"],
            "location": intervention["location"],
            "status": intervention["status"],
            "image": intervention["image"],
            "video": intervention["video"],
            "comment": intervention["comment"]
        }
        Intervention.reports.append(intervention_dict)

    return jsonify({
        'status': 200,
        'data': Intervention.reports,
        'message': 'Interventions Fetched'
    })

def update_intervention_loc(intervention_id):
    ''' Function enables the user to update a single intervention record location
    :param:
    incident_id - holds integer value of the id of the individual intervention to be updated
    :returns:
    A success message and the Details of the intervention whose id matches the one entered and update the location if the incType equal red-flag.
    '''
    validator = Incident_validation()
    no_data = validator.check_if_empty_intervention()
    not_exist = validator.check_if_intervention_exist(intervention_id)
    if no_data:
        return no_data 
    if not_exist: 
        return not_exist
    try:
        data = request.get_json()
        location = data.get("location")
        val = validator.validate_red_flag_location(location)
        if val:
            return jsonify(val), 400
            
        update_loc = db.update_intervention("interventions", "location", location, "intervention_id", intervention_id)
        user_data=db.query_one_intervention(intervention_id)
        return jsonify({
            'status': 200,
            'id': update_loc['intervention_id'],
            'data': user_data,
            'message': 'location updated successfully'
        }), 200  

    except Exception:
        return jsonify({
            'status': 400,
            'error': 'Something went wrong with your inputs or check your id in the URL'
        }), 400
