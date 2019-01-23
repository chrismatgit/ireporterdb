from flask import jsonify
from db import DatabaseConnection
import re
import os


db = DatabaseConnection()

class Validations:
    '''Class handles all user validations when signup'''
    def user_validation(self, firstname, lastname, othernames, email, phone_number, username, password):
        '''method that validate all the user inputs'''
        if not firstname or firstname == "" or not type(firstname) == str:
            return {
                'status': 400,
                'error': 'Firstname field can not be left empty and should be a string'
            }

        if not lastname or lastname == "" or not type(lastname) == str:
            return {
                'status': 400,
                'error': 'Lastname field can not be left empty and should be a string'
            }
        
        if not othernames or othernames == "" or not type(othernames) == str:
            return {
                'status': 400,
                'error': 'othernames field can not be left empty and should be a string'
            }
     
        if not email or not type(email) == str or email == "" or \
        not re.match(r"[^@.]+@[A-Za-z]+\.[a-z]+", email):
            return {
                'status': 400,
                'error': 'Email field can not be left empty, is invalid(eg: example@example.com) and should be a string'
            }
        
        if not phone_number or phone_number == "" or not type(phone_number) == str:
            return {
                'status': 400,
                'error': 'phone_number field can not be left empty and should be a string!'
            }
        
        if not username or username == "" or not type(username) == str:
            return {
                'status': 400,
                'error': 'Username field can not be left empty and should be a string'
            }
 
        if not password or password == "" or not type(password) == str:
            return {
                'status': 400,
                'error': 'Password field can not be left empty and should be a string'
            }

    @staticmethod
    def validate_signup(username, email):
        ''' Function enables to check if the user exist in the database
        :param:
        username - holds the username entered by a user and check if it matches any username in the database
        email - holds the email entered by a user and check if it matches any email in the database
        both :returns:
        a error message if true.
        '''
        db = DatabaseConnection()
        username = db.check_username(username)
        email = db.check_email(email)

        if username != None:
            return {
                'status': 409,
                'error': 'username already taken'
            }
        if email != None:
            return {
                'status': 409,
                'error': 'email already existed'
            }
        
    @staticmethod
    def check_if_user_exist(user_id): 
        if not db.query_one(user_id):
            return jsonify({
            'status': 404,
            'error': 'Please user does not exit or check your id'
        }), 404

class Login_validation:
    '''Class handles all user validations when login'''
    def exist_user_validation(self, username, password):
        '''method that validate all the login input from the user'''
        if not username or username == "" or not type(username) == str:
            return {
                'status': 400,
                'error': 'Username field can not be left empty and should be a string'
            }

        if not password or password == "" or not type(password) == str:
            return {
                'status': 400,
                'error': 'Password field can not be left empty and should be a string'
            }

class Incident_validation:
    '''Class handles all incident validations'''
    def add_incident_validation(self, createdby,location, status, image, video, comment):
        '''Method that validate all the incident input from the user'''
        # if not createdby or not isinstance(createdby, int):
        if not createdby or not isinstance(createdby, int):
            return {
                'status': 400,
                'error': 'createdby field can not be left empty and should be an integer'
                }
    
        if not location or location =="" or not isinstance(location, list) or not len(location)==2 or not isinstance(location[0], float)\
         or not isinstance(location[1], float):
            return {
                'status': 400,
                'error': 'location field can not be left empty and should be a list'
            }
        
        if not comment or not isinstance(comment, str) :
            return {
                'status': 400,
                'error': 'comment field can not be left empty and should be a string'
            }
    
        # if not status or status == "" or not status == "delivered" or not isinstance(status, str):
        #     return {
        #         'status': 400,
        #         'error':'status field can not be left empty, it should be delivered and must be a string'
        #     }
        
        extensions = [".jpg", ".png"]
        details = os.path.splitext(image)
        if details[1] not in extensions:
            return {
                'status': 400,
                'error': 'image has an invalid format(eg: image.png  or image.jpg'
            }

        extensions = [".mp4", ".avi"]
        details = os.path.splitext(video)
        if details[1] not in extensions:
            return {
                'status': 400,
                'error': 'video has an invalid format(eg: video.mp4  or video.avi)'
            }

    @staticmethod
    def check_if_empty():
        if not db.query_all("incidents"):
            return jsonify({
                'status': 404,
                'error': 'There is no incident yet'
            }), 404
    
    @staticmethod
    def check_if_empty_intervention():
        if not db.query_all("interventions"):
            return jsonify({
                'status': 404,
                'error': 'There is no incident yet'
            }), 404
            
    @staticmethod
    def check_if_red_flag_exist(incident_id): 
        if not db.query_one(incident_id):
            return jsonify({
            'status': 404,
            'error': 'Please red-flag does not exit or check your id'
        }), 404

    @staticmethod
    def check_if_intervention_exist(intervention_id): 
        if not db.query_one_intervention(intervention_id):
            return jsonify({
            'status': 404,
            'error': 'Please intervention does not exit or check your id'
        }), 404

    @staticmethod
    def validate_red_flag_inctype(inctype):
        if not inctype or inctype == "" or not inctype == "red-flag" or not isinstance(inctype, str):
            return {
                'status': 400,
                'error': 'incType field can not be left empty, it should be eg: red-flag should be a string'
            }

    @staticmethod
    def validate_intervention_type(inctype):
        if not inctype or inctype == "" or not inctype == "intervention" or not isinstance(inctype, str):
            return {
                'status': 400,
                'error': 'incType field can not be left empty, it should be eg: intervention should be a string'
            }

    @staticmethod
    def validate_red_flag_comment(comment):
        if not comment or comment == "" or not isinstance(comment, str) :
            return {
                'status': 400,
                'error': 'comment field can not be left empty and should be a string'
            }
            
    @staticmethod
    def validate_red_flag_location(location):
        if not location or location == "" or not isinstance(location, list) \
        or not len(location)==2 or not isinstance(location[0], float) or not isinstance(location[1], float):
            return {
                'status': 400,
                'error': 'location field can not be left empty and should be a list'
            }

    @staticmethod
    def validate_status(status):
        if not status or status == "" or not status == "under_investigation" and not status== "rejected"\
            and not status=="resolved" or not isinstance(status, str):
            return {
                'status': 400,
                'error':'status field can not be left empty, it should be eg: resolved, under_investigation or rejected and should be a string'
            }