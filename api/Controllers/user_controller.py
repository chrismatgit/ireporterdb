from flask import Flask, jsonify, request
from db import DatabaseConnection
from api.Models.Users import User
from api.Utilities.validations import Validations, Login_validation
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
        firstname = data.get("firstname")
        lastname = data.get("lastname")
        othernames = data.get("othernames")
        email = data.get("email")
        phone_number = data.get("phone_number")
        username = data.get("username")
        password = data.get("password")
        isadmin = data.get("isadmin")

        # validations
        validator = Validations()
        invalid_data = validator.user_validation(firstname, lastname, \
        othernames, email, phone_number, username, password)
        invalid = validator.validate_signup(username, email)
        if invalid_data:
            return jsonify(invalid_data), 400
        if not invalid:
            new_user = db.user_signup(firstname, lastname, othernames, email, phone_number, \
            username, password, isadmin)         
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


def admin_signup():
    '''Function creates a new admin user to the database
    :returns:
    a success message if successful else the error
    '''
    try:
        data = request.get_json()
        firstname = data.get("firstname")
        lastname = data.get("lastname")
        othernames = data.get("othernames")
        email = data.get("email")
        phone_number = data.get("phone_number")
        username = data.get("username")
        password = data.get("password")
        isadmin = data.get("isadmin")

        # validations
        validator = Validations()
        invalid_data = validator.user_validation(firstname, lastname, othernames, email, phone_number, username, password)
        invalid = validator.validate_signup(username, email)
        if invalid_data:
            return jsonify(invalid_data), 400
        if not invalid:
            new_user = db.admin_signup(firstname, lastname, othernames, email, phone_number, username, password, isadmin)         
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

def login():
    '''Function allows a user to login after sign up
    :returns:
    a success message with the username and token
    '''
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        validator = Login_validation()
        invalid_data = validator.exist_user_validation(username, password)
        if not db.query_all("user"):
            return jsonify({
                'status': 404,
                'error': 'There is no user yet'
            }), 404
        if invalid_data:
            return jsonify(invalid_data), 400
        user = db.login(username)
        if user != None:
            if user["username"]== username and user["password"] == password:
                user_id = user["user_id"]
                expires = datetime.timedelta(days=1)
                token = create_access_token(user_id, expires_delta=expires)
                return jsonify({
                    "status": 200,
                    "token": token,
                    "message": f"{username} successfuly login"
                }), 200
            else:
                return jsonify({
                    "status": 400,
                    "error": "Wrong username or password"
                }), 400
        else:
            return jsonify({
                "status": 400,
                "error": "Wrong username or password"
            }), 400
    except Exception:
        return jsonify({
            'status': 400,
            'error': 'Something went wrong with your inputs'
        }), 400

def get_all_users():
    ''' Function enables the view of all the users
    :returns:
    A list of all the account created
    ''' 
    if not db.query_all("users"):
        return jsonify({
            'status': 404,
            'error': 'There are no user yet'
        }), 404
    accounts = db.query_all("users")
    for account in accounts:
        account_dict = {
            "user_id": account["user_id"],
            "firstname": account["firstname"],
            "lastname": account["lastname"],
            "othernames": account["othernames"],
            "email": account["email"],
            "phone_number": account["phone_number"],
            "username": account["username"],
            "password": account["password"],
            "registered": account["registered"],
            "isadmin": account["isadmin"]
        }
        User.accounts.append(account_dict)
    return jsonify({
        'status': 200,
        'Data': User.accounts,
        'message': 'Accounts fetched'
    }), 200