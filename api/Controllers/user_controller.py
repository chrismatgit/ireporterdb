from flask import Flask, jsonify, request
from db import DatabaseConnection
from api.Models.Users import User
from api.Utilities.validations import Validations
from flask_jwt_extended import create_access_token
import datetime

db = DatabaseConnection()
validator = Validations()
def signup():
    '''Function creates a new user to the database
    :returns:
    a success message if successful else the error
    '''
    try:
        data = request.get_json()
        # user_id = len(User.accounts)+1
        firstname = data.get("firstname")
        lastname = data.get("lastname")
        othernames = data.get("othernames")
        email = data.get("email")
        phone_number = data.get("phone_number")
        username = data.get("username")
        password = data.get("password")
        registered = data.get("registered")
        isadmin = data.get("isadmin")

        # validations
        invalid_data = validator.user_validation(firstname, lastname, othernames, email, phone_number, username, password)
        invalid = validator.validate_signup(username, email)
        if invalid_data:
            return jsonify(invalid_data), 400
        if not invalid:
            new_user = db.user_signup(firstname, lastname, othernames, email, phone_number, username, password, registered, isadmin)         
            return jsonify({
                "status": 201,
                "data": new_user,
                "message": f"{firstname} has been created successfuly"
            }), 201
                                    
        return jsonify(invalid), 409

    except Exception:
        return jsonify({
            'status': 400,
            'error': 'Something went wrong with your inputs'
        }), 400