
from flask import Flask, jsonify, request
from db import DatabaseConnection
from api.Models.Incidents import Incident
from api.Utilities.validations import Incident_validation
from flask_jwt_extended import get_jwt_identity
import datetime

db = DatabaseConnection()

def create_red_flag():
    '''Function creates a new red-flag to the database
    :returns:
    a success message and the red-flag.
    '''
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        createdon = datetime.datetime.now()
        createdby = current_user
        inctype = data.get("inctype")
        location = data.get("location")
        status = "delivered"
        image = data.get("image")
        video = data.get("video")
        comment = data.get("comment")
        # validation
        validator = Incident_validation()
        invalid_data = validator.add_incident_validation(location,status,image,video,comment)
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
    ''' Function enables the user to get a single red-flag record
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
    incident = db.query_one(incident_id)
    return jsonify({
        'status': 200,
        'data': incident,
        'message': 'Red-Flag Fetched'
        }), 200

def get_all_red_flags():
    ''' Function enables the view of all the red-flag
    :returns:
    A list of all the red-flag created
    '''
    validator = Incident_validation()
    no_data = validator.check_if_empty()
    if no_data:
        return no_data 
    incidents = db.query_all("incidents")
    for incident in incidents:
        incident_dict = {
            "incident_id": incident["incident_id"],
            "createdon": incident["createdon"],
            "createdby": incident["createdby"],
            "inctype": incident["inctype"],
            "location": incident["location"],
            "status": incident["status"],
            "image": incident["image"],
            "video": incident["video"],
            "comment": incident["comment"]
        }
        Incident.reports.append(incident_dict)

    return jsonify({
        'status': 200,
        'data': Incident.reports,
        'message': 'Red-flags Fetched'
    })


def update_red_flag_loc(incident_id):
    ''' Function enables the user to update a single red-flag record location
    :param:
    incident_id - holds integer value of the id of the individual red-flag to be updated
    :returns:
    A success message and the Details of the red-flag whose id matches the one entered and update the location if the incType equal red-flag.
    '''
    
    try:
        validator = Incident_validation()
        no_data = validator.check_if_empty()
        not_exist = validator.check_if_red_flag_exist(incident_id)
        if no_data:
            return no_data 
        if not_exist: 
            return not_exist
        data = request.get_json()
        location = data.get("location")
        val = validator.validate_red_flag_location(location)
        if val:
            return jsonify(val), 400
            
        update_loc = db.update("incidents", "location", location, "incident_id", incident_id)
        user_data=db.query_one(incident_id)
        return jsonify({
            'status': 200,
            'id': update_loc['incident_id'],
            'data': user_data,
            'message': 'location updated successfully'
        }), 200  

    except Exception:
        return jsonify({
            'status': 400,
            'error': 'Something went wrong with your inputs or check your id in the URL'
        }), 400

def update_red_flag_com(incident_id):
    ''' Function enables the user to update a single red-flag record comment
    :param:
    incident_id - holds integer value of the id of the individual red-flag to be updated
    :returns:
    A success message and the Details of the red-flag whose id matches the one entered and update the comment if the incType equal red-flag.
    '''
    try:
        validator = Incident_validation()
        no_data = validator.check_if_empty()
        not_exist = validator.check_if_red_flag_exist(incident_id)
        if no_data:
            return no_data 
        if not_exist: 
            return not_exist
    
        data = request.get_json()
        comment = data.get("comment")
        val = Incident_validation.validate_red_flag_comment(comment)
        if not val:
            new_incident= db.update("incidents", "comment", comment, "incident_id", incident_id)
            user_data=db.query_one(incident_id)
            return jsonify({
                'status': 200,
                'id': new_incident['incident_id'],
                'data': user_data,
                'message': 'comment updated successfully'
            })
        else:
            return jsonify(val), 400
    except Exception:
        return jsonify({
            'status': 400,
            'error': 'Something went wrong with your inputs or check your id in the URL'
        }), 400

def delete_red_flag(incident_id):
    ''' Function enables a user to delete a single red-flag record
    :param:
    incident_id - holds integer value of the id of the individual red-flag to be deleted
    :returns:
    the success message and the Details of the incident whose id matches the one entered to be deleted.
    '''
    validator = Incident_validation()
    no_data = validator.check_if_empty()
    not_exist = validator.check_if_red_flag_exist(incident_id)
    if no_data:
        return no_data 
    if not_exist: 
        return not_exist
    try:
        user_data=db.query_one(incident_id)
        delete_inc = db.delete("incidents", "incident_id", incident_id)
        return jsonify({
            'status': 200,
            'id': delete_inc["incident_id"],
            'data': user_data,
            'message': 'incident deleted'
        }), 200
    except Exception:
        return jsonify({
            'message': 'something went wrong Or check your id',
            'status': 404
        }), 404
        
def update_red_flag_status(incident_id):
    ''' Function enables a user to update a single red-flag record status
    :param:
    incident_id - holds integer value of the id of the individual red-flag to be updated
    :returns:
    the success message and the Details of the incident whose id matches the one entered to be updated.
    '''
    try:
        validator = Incident_validation()
        no_data = validator.check_if_empty()
        not_exist = validator.check_if_red_flag_exist(incident_id)
        if no_data:
            return no_data 
        if not_exist: 
            return not_exist
    
        data = request.get_json()
        status = data.get("status")
        val = Incident_validation.validate_status(status)
        if not val:
            updated_incident= db.update("incidents", "status", status, "incident_id", incident_id)
            user_data=db.query_one(incident_id)
            return jsonify({
                'status': 200,
                'id': updated_incident['incident_id'],
                'data': user_data,
                'message': 'status updated successfully'
            })
        else:
            return jsonify(val), 400
        # else:
        #     return jsonify(validator), 400
    except Exception:
        return jsonify({
            'status': 400,
            'error': 'Something went wrong with your inputs or check your id in the URL'
        }), 400