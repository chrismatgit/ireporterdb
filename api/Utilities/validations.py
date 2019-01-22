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
