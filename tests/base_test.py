import json
import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from api import app
from api.Models import Users
from db import DatabaseConnection


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)
        self.db = DatabaseConnection()

    def login_user(self):
        """Base method for logging in a user"""
        account = {
            "email": "kelly1212@example.com",
            "firstname": "mary",
            "isadmin": True,
            "lastname": "grace",
            "othernames": "kelly",
            "password": "password",
            "phone_number": "07512345678",
            "registered": "2019-01-22 23:51:33.866191",
            "username": "kellyma1212"
        }
        response = self.tester.post(
            '/api/v1/auth/signup/admin',
            content_type='application/json',
            data=json.dumps(account)
        )
        account = dict(
            username='kellyma1212',
            password='password'
        )
        response = self.tester.post(
            '/api/v1/auth/login',
            content_type='application/json',
            data=json.dumps(account)
        )
        reply = json.loads(response.data.decode())
        return reply