import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
import json
from api import app
from api.Models.Intervention import Intervention
from api.Controllers.intervention_controller import create_intervention, get_unique_intervention, get_all_interventions, \
update_intervention_loc, update_intervention_com, update_intervention_status, delete_intervention
from db import DatabaseConnection
from base_test import BaseTest

class Test_Incident(BaseTest):
    def setUp(self):
        self.tester = app.test_client(self)
        self.db = DatabaseConnection()

    def test_create_intervention(self):
        reply = self.login_user()
        token = reply['token']
        report = {
            "comment": "No comment",
            "createdby": 1,
            "createdon": "Thu, 13 Dec 2018 08:33:24 GMT",
            "image": "img.jpg",
            "inctype": "intervention",
            "location": [12112.01,12122.454],
            "status": "delivered",
            "video": "video.avi"
        }
        response = self.tester.post(
            '/api/v1/interventions', content_type='application/json',
            data = json.dumps(report), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
        self.assertIn("intervention has been created successfuly", reply['message'])
        self.assertEqual(response.status_code, 201)

    def test_create_comment_is_empty(self):
        reply = self.login_user()
        token = reply['token']
        report = {
            "comment": "",
            "createdby": 1,
            "createdon": "Thu, 13 Dec 2018 08:33:24 GMT",
            "image": "img.jpg",
            "inctype": "intervention",
            "location": [12112.01,12122.454],
            "status": "delivered",
            "video": "video.avi"
        }
        response = self.tester.post(
            '/api/v1/interventions', content_type='application/json',
            data = json.dumps(report), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)

    def test_create_comment_is_not_a_string(self):
        reply = self.login_user()
        token = reply['token']
        report = {
            "comment": True,
            "createdby": 1,
            "createdon": "Thu, 13 Dec 2018 08:33:24 GMT",
            "image": "img.jpg",
            "inctype": "intervention",
            "location": [12112.01,12122.454],
            "status": "delivered",
            "video": "video.avi"
        }
        response = self.tester.post(
            '/api/v1/interventions', content_type='application/json',
            data = json.dumps(report), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)

    def test_create_location_is_not_a_string(self):
        reply = self.login_user()
        token = reply['token']
        report = {
            "comment": "some comment",
            "createdby": 1,
            "createdon": "Thu, 13 Dec 2018 08:33:24 GMT",
            "image": "img.jpg",
            "inctype": "intervention",
            "location": 101010,
            "status": "delivered",
            "video": "video.avi"
        }
        response = self.tester.post(
            '/api/v1/interventions', content_type='application/json',
            data = json.dumps(report), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
        self.assertIn("location field can not be left empty and should be a list", reply['error'])
        self.assertEqual(response.status_code, 400)

    def test_create_location_is_empty(self):
        reply = self.login_user()
        token = reply['token']
        report = {
            "comment": "some comment",
            "createdby": 1,
            "createdon": "Thu, 13 Dec 2018 08:33:24 GMT",
            "image": "img.jpg",
            "inctype": "intervention",
            "location": "",
            "status": "delivered",
            "video": "video.avi"
        }
        response = self.tester.post(
            '/api/v1/interventions', content_type='application/json',
            data = json.dumps(report), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
        self.assertIn("location field can not be left empty and should be a list", reply['error'])
        self.assertEqual(response.status_code, 400)

    def test_image_has_an_invalid_format(self):
        reply = self.login_user()
        token = reply['token']
        report = {
            "comment": "some comment",
            "createdby": 1,
            "createdon": "Thu, 13 Dec 2018 08:33:24 GMT",
            "image": "img.xls",
            "inctype": "intervention",
            "location": [12112.01,12122.454],
            "status": "delivered",
            "video": "video.avi"
        }
        response = self.tester.post(
            '/api/v1/interventions', content_type='application/json',
            data = json.dumps(report), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
        self.assertIn("image has an invalid format(eg: image.png  or image.jpg", reply['error'])
        self.assertEqual(response.status_code, 400)

    def test_image_has_an_empty_name(self):
        reply = self.login_user()
        token = reply['token']
        report = {
            "comment": "some comment",
            "createdby": 1,
            "createdon": "Thu, 13 Dec 2018 08:33:24 GMT",
            "image": ".jpg",
            "inctype": "intervention",
            "location": [12112.01,12122.454],
            "status": "delivered",
            "video": "video.avi"
        }
        response = self.tester.post(
            '/api/v1/interventions', content_type='application/json',
            data = json.dumps(report), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
        self.assertIn("image has an invalid format(eg: image.png  or image.jpg", reply['error'])
        self.assertEqual(response.status_code, 400)

    def test_image_has_a_invalid_input(self):
        reply = self.login_user()
        token = reply['token']
        report = {
            "comment": "some comment",
            "createdby": 1,
            "createdon": "Thu, 13 Dec 2018 08:33:24 GMT",
            "image": True,
            "inctype": "intervention",
            "location": [12112.01,12122.454],
            "status": "delivered",
            "video": "video.avi"
        }
        response = self.tester.post(
            '/api/v1/interventions', content_type='application/json',
            data = json.dumps(report), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
        self.assertIn("Something went wrong with your inputs", reply['error'])
        self.assertEqual(response.status_code, 400)


    def test_video_has_invalid_format(self):
        reply = self.login_user()
        token = reply['token']
        report = {
            "comment": "some comment",
            "createdby": 1,
            "createdon": "Thu, 13 Dec 2018 08:33:24 GMT",
            "image": "image.jpg",
            "inctype": "intervention",
            "location": [12112.01,12122.454],
            "status": "delivered",
            "video": "video.xls"
        }
        response = self.tester.post(
            '/api/v1/interventions', content_type='application/json',
            data = json.dumps(report), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
        self.assertIn("video has an invalid format(eg: video.mp4  or video.avi)", reply['error'])
        self.assertEqual(response.status_code, 400)

    def test_video_has_an_invalid_name(self):
        reply = self.login_user()
        token = reply['token']
        report = {
            "comment": "some comment",
            "createdby": 1,
            "createdon": "Thu, 13 Dec 2018 08:33:24 GMT",
            "image": "image.jpg",
            "inctype": "intervention",
            "location": [12112.01,12122.454],
            "status": "delivered",
            "video": ".avi"
        }
        response = self.tester.post(
            '/api/v1/interventions', content_type='application/json',
            data = json.dumps(report), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
        self.assertIn("video has an invalid format(eg: video.mp4  or video.avi)", reply['error'])
        self.assertEqual(response.status_code, 400)

    def test_video_has_invalid_input(self):
        reply = self.login_user()
        token = reply['token']
        report = {
            "comment": "some comment",
            "createdby": 1,
            "createdon": "Thu, 13 Dec 2018 08:33:24 GMT",
            "image": "image.jpg",
            "inctype": "intervention",
            "location": [12112.01,12122.454],
            "status": "delivered",
            "video": True
        }
        response = self.tester.post(
            '/api/v1/interventions', content_type='application/json',
            data = json.dumps(report), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
        self.assertIn("Something went wrong with your inputs", reply['error'])
        self.assertEqual(response.status_code, 400)

    def test_inctype_is_empty(self):
        reply = self.login_user()
        token = reply['token']
        report = {
            "comment": "some comment",
            "createdby": 1,
            "createdon": "Thu, 13 Dec 2018 08:33:24 GMT",
            "image": "image.jpg",
            "inctype": "",
            "location": [12112.01,12122.454],
            "status": "delivered",
            "video": "video.mp4"
        }
        response = self.tester.post(
            '/api/v1/interventions', content_type='application/json',
            data = json.dumps(report), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
     
        self.assertIn("incType field can not be left empty, it should be eg: intervention should be a string", reply['error'])
        self.assertEqual(response.status_code, 400)

    def test_inctype_is_not_a_string(self):
        reply = self.login_user()
        token = reply['token']
        report = {
            "comment": "some comment",
            "createdby": 1,
            "createdon": "Thu, 13 Dec 2018 08:33:24 GMT",
            "image": "image.jpg",
            "inctype": 1215,
            "location": [12112.01,12122.454],
            "status": "delivered",
            "video": "video.mp4"
        }
        response = self.tester.post(
            '/api/v1/interventions', content_type='application/json',
            data = json.dumps(report), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
        self.assertIn("incType field can not be left empty, it should be eg: intervention should be a string", reply['error'])
        self.assertEqual(response.status_code, 400)

    def test_inctype_is_not_red_flag_or_intervention(self):
        reply = self.login_user()
        token = reply['token']
        report = {
            "comment": "some comment",
            "createdby": 1,
            "createdon": "Thu, 13 Dec 2018 08:33:24 GMT",
            "image": "image.jpg",
            "inctype": "crime",
            "location": [12112.01,12122.454],
            "status": "delivered",
            "video": "video.mp4"
        }
        response = self.tester.post(
            '/api/v1/interventions', content_type='application/json',
            data = json.dumps(report), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
        self.assertIn("incType field can not be left empty, it should be eg: intervention should be a string", reply['error'])
        self.assertEqual(response.status_code, 400)

    def test_status_is_delivered(self):
        reply = self.login_user()
        token = reply['token']
        report = {
            "comment": "No comment",
            "createdby": 1,
            "createdon": "Thu, 13 Dec 2018 08:33:24 GMT",
            "image": "img.jpg",
            "inctype": "intervention",
            "location": [12112.01,12122.454],
            "status": "delivered",
            "video": "video.avi"
        }
        response = self.tester.post(
            '/api/v1/interventions', content_type='application/json',
            data = json.dumps(report), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
        self.assertIn("intervention has been created successfuly", reply['message'])
        self.assertEqual(response.status_code, 201)
    
    def test_get_unique_incident(self):
        reply = self.login_user()
        token = reply['token']
        report = {
            "comment": "No comment",
            "createdby": 1,
            "createdon": "Thu, 13 Dec 2018 08:33:24 GMT",
            "image": "img.jpg",
            "inctype": "intervention",
            "location": [12112.01,12122.454],
            "status": "delivered",
            "video": "video.avi"
        }
        response = self.tester.post(
            '/api/v1/interventions', content_type='application/json',
            data = json.dumps(report), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
     
        self.assertIn("intervention has been created successfuly", reply['message'])
        self.assertEqual(response.status_code, 201)
        response = self.tester.get(
            '/api/v1/interventions/1', content_type='application/json', headers={'Authorization': f'Bearer {token}'}
        )
        self.assertEqual(response.status_code, 200)

    def test_inexisted_id(self):
        reply = self.login_user()
        token = reply['token']
        report = {
            "comment": "No comment",
            "createdby": 1,
            "createdon": "Thu, 13 Dec 2018 08:33:24 GMT",
            "image": "img.jpg",
            "inctype": "intervention",
            "location": [12112.01,12122.454],
            "status": "delivered",
            "video": "video.avi"
        }
        response = self.tester.post(
            '/api/v1/interventions', content_type='application/json',
            data = json.dumps(report), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
        self.assertIn("intervention has been created successfuly", reply['message'])
        self.assertEqual(response.status_code, 201)
        response = self.tester.get(
            '/api/v1/interventions/122', content_type='application/json', headers={'Authorization': f'Bearer {token}'}
        )
        self.assertEqual(response.status_code, 404)

    def test_no_incident_yet(self):
        reply = self.login_user()
        token = reply['token']
        response = self.tester.get(
            '/api/v1/interventions/1', content_type='application/json', headers={'Authorization': f'Bearer {token}'}
        )
        self.assertEqual(response.status_code, 404)

    def test_get_all_incident(self):
        reply = self.login_user()
        token = reply['token']
        report = {
            "comment": "No comment",
            "createdby": 1,
            "createdon": "Thu, 13 Dec 2018 08:33:24 GMT",
            "image": "img.jpg",
            "inctype": "intervention",
            "location": [12112.01,12122.454],
            "status": "delivered",
            "video": "video.avi"
        }
        response = self.tester.post(
            '/api/v1/interventions', content_type='application/json',
            data = json.dumps(report), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
     
        self.assertIn("intervention has been created successfuly", reply['message'])
        self.assertEqual(response.status_code, 201)
        response = self.tester.get(
            '/api/v1/interventions', content_type='application/json', headers={'Authorization': f'Bearer {token}'}
        )
        self.assertEqual(response.status_code, 200)

    def test_update_location(self):
        reply = self.login_user()
        token = reply['token']
        report = {
            "comment": "No comment",
            "createdby": 1,
            "createdon": "Thu, 13 Dec 2018 08:33:24 GMT",
            "image": "img.jpg",
            "inctype": "intervention",
            "location": [12112.01,12122.454],
            "status": "under_investigation",
            "video": "video.avi"
        }
        response = self.tester.post(
            '/api/v1/interventions', content_type='application/json',
            data = json.dumps(report), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
        self.assertIn("intervention has been created successfuly", reply['message'])
        self.assertEqual(response.status_code, 201)

        update_location = { "location": [11212.63666, 578564.36]}
        response = self.tester.patch(
            '/api/v1/interventions/1/location', content_type='application/json',
            data = json.dumps(update_location), headers = {'Authorization':f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
        self.assertIn(reply["message"], "location updated successfully")
        self.assertEqual(response.status_code, 200)

    def test_update_location_with_wrong_id(self):
        reply = self.login_user()
        token = reply['token']
        report = {
            "comment": "No comment",
            "createdby": 1,
            "createdon": "Thu, 13 Dec 2018 08:33:24 GMT",
            "image": "img.jpg",
            "inctype": "intervention",
            "location": [12112.01,12122.454],
            "status": "under_investigation",
            "video": "video.avi"
        }
        response = self.tester.post(
            '/api/v1/interventions', content_type='application/json',
            data = json.dumps(report), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
        self.assertIn("intervention has been created successfuly", reply['message'])
        self.assertEqual(response.status_code, 201)

        update_location = { "location": [11212.63666, 578564.36]}
        response = self.tester.patch(
            '/api/v1/interventions/12/location', content_type='application/json',
            data = json.dumps(update_location), headers = {'Authorization':f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
        self.assertIn(reply["error"], "Please intervention does not exit or check your id")
        self.assertEqual(response.status_code, 404)


    def test_update_location_is_empty(self):
        reply = self.login_user()
        token = reply['token']
        report = {
            "comment": "No comment",
            "createdby": 1,
            "createdon": "Thu, 13 Dec 2018 08:33:24 GMT",
            "image": "img.jpg",
            "inctype": "intervention",
            "location": [12112.01,12122.454],
            "status": "under_investigation",
            "video": "video.avi"
        }
        response = self.tester.post(
            '/api/v1/interventions', content_type='application/json',
            data = json.dumps(report), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
        self.assertIn("intervention has been created successfuly", reply['message'])
        self.assertEqual(response.status_code, 201)

        update_location = { "location": ""}
        response = self.tester.patch(
            '/api/v1/interventions/1/location', content_type='application/json',
            data = json.dumps(update_location), headers = {'Authorization':f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
        self.assertIn(reply["error"], "location field can not be left empty and should be a list")
        self.assertEqual(response.status_code, 400)

    def test_update_location_with_wrong_id_(self):
        reply = self.login_user()
        token = reply['token']
        report = {
            "comment": "No comment",
            "createdby": 1,
            "createdon": "Thu, 13 Dec 2018 08:33:24 GMT",
            "image": "img.jpg",
            "inctype": "intervention",
            "location": [12112.01,12122.454],
            "status": "under_investigation",
            "video": "video.avi"
        }
        response = self.tester.post(
            '/api/v1/interventions', content_type='application/json',
            data = json.dumps(report), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
        self.assertIn("intervention has been created successfuly", reply['message'])
        self.assertEqual(response.status_code, 201)

        update_location = { "location": [11212.63666, 578564.36]}
        response = self.tester.patch(
            '/api/v1/interventions/12/location', content_type='application/json',
            data = json.dumps(update_location), headers = {'Authorization':f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
        self.assertIn(reply["error"], "Please intervention does not exit or check your id")
        self.assertEqual(response.status_code, 404)

    def test_update_location_with_wrong_input(self):
        reply = self.login_user()
        token = reply['token']
        report = {
            "comment": "No comment",
            "createdby": 1,
            "createdon": "Thu, 13 Dec 2018 08:33:24 GMT",
            "image": "img.jpg",
            "inctype": "intervention",
            "location": [12112.01,12122.454],
            "status": "under_investigation",
            "video": "video.avi"
        }
        response = self.tester.post(
            '/api/v1/interventions', content_type='application/json',
            data = json.dumps(report), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
        self.assertIn("intervention has been created successfuly", reply['message'])
        self.assertEqual(response.status_code, 201)

        update_location = [{ "location": [12.2,112.5]}]
        response = self.tester.patch(
            '/api/v1/interventions/1/location', content_type='application/json',
            data = json.dumps(update_location), headers = {'Authorization':f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
        self.assertIn(reply["error"], "Something went wrong with your inputs or check your id in the URL")
        self.assertEqual(response.status_code, 400)

    def test_update_location_is_not_string(self):
        reply = self.login_user()
        token = reply['token']
        report = {
            "comment": "No comment",
            "createdby": 1,
            "createdon": "Thu, 13 Dec 2018 08:33:24 GMT",
            "image": "img.jpg",
            "inctype": "intervention",
            "location": [12112.01,12122.454],
            "status": "under_investigation",
            "video": "video.avi"
        }
        response = self.tester.post(
            '/api/v1/interventions', content_type='application/json',
            data = json.dumps(report), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
        self.assertIn("intervention has been created successfuly", reply['message'])
        self.assertEqual(response.status_code, 201)

        update_location = { "location": {}}
        response = self.tester.patch(
            '/api/v1/interventions/1/location', content_type='application/json',
            data = json.dumps(update_location), headers = {'Authorization':f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
        self.assertIn(reply["error"], "location field can not be left empty and should be a list")
        self.assertEqual(response.status_code, 400)

    def test_update_comment_is_valid(self):
        reply = self.login_user()
        token = reply['token']
        report = {
            "comment": "No comment",
            "createdby": 1,
            "createdon": "Thu, 13 Dec 2018 08:33:24 GMT",
            "image": "img.jpg",
            "inctype": "intervention",
            "location": [12112.01,12122.454],
            "status": "under_investigation",
            "video": "video.avi"
        }
        response = self.tester.post(
            '/api/v1/interventions', content_type='application/json',
            data = json.dumps(report), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
     
        self.assertIn("intervention has been created successfuly", reply['message'])
        self.assertEqual(response.status_code, 201)
        update_comment = { "comment": " test comment"}
        response = self.tester.patch(
            '/api/v1/interventions/1/comment', content_type='application/json',
            data = json.dumps(update_comment), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
        self.assertIn(reply["message"], "comment updated successfully")
        self.assertEqual(response.status_code, 200)

    def test_update_comment_is_empty(self):
        reply = self.login_user()
        token = reply['token']
        report = {
            "comment": "No comment",
            "createdby": 1,
            "createdon": "Thu, 13 Dec 2018 08:33:24 GMT",
            "image": "img.jpg",
            "inctype": "intervention",
            "location": [12112.01,12122.454],
            "status": "under_investigation",
            "video": "video.avi"
        }
        response = self.tester.post(
            '/api/v1/interventions', content_type='application/json',
            data = json.dumps(report), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
     
        self.assertIn("intervention has been created successfuly", reply['message'])
        self.assertEqual(response.status_code, 201)
        update_comment = { "comment": ""}
        response = self.tester.patch(
            '/api/v1/interventions/1/comment', content_type='application/json',
            data = json.dumps(update_comment), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
        self.assertIn(reply["error"], "comment field can not be left empty and should be a string")
        self.assertEqual(response.status_code, 400)


    def test_update_comment_with_wrong_input(self):
        reply = self.login_user()
        token = reply['token']
        report = {
            "comment": "No comment",
            "createdby": 1,
            "createdon": "Thu, 13 Dec 2018 08:33:24 GMT",
            "image": "img.jpg",
            "inctype": "intervention",
            "location": [12112.01,12122.454],
            "status": "under_investigation",
            "video": "video.avi"
        }
        response = self.tester.post(
            '/api/v1/interventions', content_type='application/json',
            data = json.dumps(report), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
     
        self.assertIn("intervention has been created successfuly", reply['message'])
        self.assertEqual(response.status_code, 201)
        update_comment = [{ "comment": ""}]
        response = self.tester.patch(
            '/api/v1/interventions/1/comment', content_type='application/json',
            data = json.dumps(update_comment), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
        self.assertIn(reply["error"], "Something went wrong with your inputs or check your id in the URL")
        self.assertEqual(response.status_code, 400)

    def test_update_comment_with_wrong_id(self):
        reply = self.login_user()
        token = reply['token']
        report = {
            "comment": "No comment",
            "createdby": 1,
            "createdon": "Thu, 13 Dec 2018 08:33:24 GMT",
            "image": "img.jpg",
            "inctype": "intervention",
            "location": [12112.01,12122.454],
            "status": "under_investigation",
            "video": "video.avi"
        }
        response = self.tester.post(
            '/api/v1/interventions', content_type='application/json',
            data = json.dumps(report), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
     
        self.assertIn("intervention has been created successfuly", reply['message'])
        self.assertEqual(response.status_code, 201)
        update_comment = { "comment": "cggfgf"}
        response = self.tester.patch(
            '/api/v1/interventions/12/comment', content_type='application/json',
            data = json.dumps(update_comment), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
        self.assertIn(reply["error"], "Please intervention does not exit or check your id")
        self.assertEqual(response.status_code, 404)


    def test_update_comment_is_not_string(self):
        reply = self.login_user()
        token = reply['token']
        report = {
            "comment": "No comment",
            "createdby": 1,
            "createdon": "Thu, 13 Dec 2018 08:33:24 GMT",
            "image": "img.jpg",
            "inctype": "intervention",
            "location": [12112.01,12122.454],
            "status": "under_investigation",
            "video": "video.avi"
        }
        response = self.tester.post(
            '/api/v1/interventions', content_type='application/json',
            data = json.dumps(report), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
     
        self.assertIn("intervention has been created successfuly", reply['message'])
        self.assertEqual(response.status_code, 201)
        update_comment = { "comment": False}
        response = self.tester.patch(
            '/api/v1/interventions/1/comment', content_type='application/json',
            data = json.dumps(update_comment), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
        self.assertIn(reply["error"], "comment field can not be left empty and should be a string")
        self.assertEqual(response.status_code, 400)

    def test_update_comment_with_invalid(self):
        reply = self.login_user()
        token = reply['token']
        report = {
            "comment": "No comment",
            "createdby": 1,
            "createdon": "Thu, 13 Dec 2018 08:33:24 GMT",
            "image": "img.jpg",
            "inctype": "intervention",
            "location": [12112.01,12122.454],
            "status": "under_investigation",
            "video": "video.avi"
        }
        response = self.tester.post(
            '/api/v1/interventions', content_type='application/json',
            data = json.dumps(report), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
     
        self.assertIn("intervention has been created successfuly", reply['message'])
        self.assertEqual(response.status_code, 201)
        update_comment = { "comment": "chris"}
        response = self.tester.patch(
            '/api/v1/interventions/12/comment', content_type='application/json',
            data = json.dumps(update_comment), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
        self.assertIn(reply["error"], "Please intervention does not exit or check your id")
        self.assertEqual(response.status_code, 404)


    def test_update_status_is_invalid(self):
        reply = self.login_user()
        token = reply['token']
        report = {
            "comment": "No comment",
            "createdby": 1,
            "createdon": "Thu, 13 Dec 2018 08:33:24 GMT",
            "image": "img.jpg",
            "inctype": "intervention",
            "location": [12112.01,12122.454],
            "status": "under_investigation",
            "video": "video.avi"
        }
        response = self.tester.post(
            '/api/v1/interventions', content_type='application/json',
            data = json.dumps(report), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
     
        self.assertIn("intervention has been created successfuly", reply['message'])
        self.assertEqual(response.status_code, 201)
        update_status = { "status": False}
        response = self.tester.patch(
            '/api/v1/interventions/1/status', content_type='application/json',
            data = json.dumps(update_status), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
        self.assertIn(reply["error"], "status field can not be left empty, it should be eg: resolved, under_investigation or rejected and should be a string")
        self.assertEqual(response.status_code, 400)


    def test_update_status_with_wrong_input(self):
        reply = self.login_user()
        token = reply['token']
        report = {
            "comment": "No comment",
            "createdby": 1,
            "createdon": "Thu, 13 Dec 2018 08:33:24 GMT",
            "image": "img.jpg",
            "inctype": "intervention",
            "location": [12112.01,12122.454],
            "status": "under_investigation",
            "video": "video.avi"
        }
        response = self.tester.post(
            '/api/v1/interventions', content_type='application/json',
            data = json.dumps(report), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
     
        self.assertIn("intervention has been created successfuly", reply['message'])
        self.assertEqual(response.status_code, 201)
        update_status = { "status": False}
        response = self.tester.patch(
            '/api/v1/interventions/1/status', content_type='application/json',
            data = json.dumps(update_status), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
        self.assertIn(reply["error"], "status field can not be left empty, it should be eg: resolved, under_investigation or rejected and should be a string")
        self.assertEqual(response.status_code, 400)

    def test_update_status_with_wrong_input_(self):
        reply = self.login_user()
        token = reply['token']
        report = {
            "comment": "No comment",
            "createdby": 1,
            "createdon": "Thu, 13 Dec 2018 08:33:24 GMT",
            "image": "img.jpg",
            "inctype": "intervention",
            "location": [12112.01,12122.454],
            "status": "under_investigation",
            "video": "video.avi"
        }
        response = self.tester.post(
            '/api/v1/interventions', content_type='application/json',
            data = json.dumps(report), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
     
        self.assertIn("intervention has been created successfuly", reply['message'])
        self.assertEqual(response.status_code, 201)
        update_status = [{ "status": "rejected"}]
        response = self.tester.patch(
            '/api/v1/interventions/1/status', content_type='application/json',
            data = json.dumps(update_status), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
        self.assertIn(reply["error"], "Something went wrong with your inputs or check your id in the URL")
        self.assertEqual(response.status_code, 400)

    
    def test_update_status_with_wrong_id(self):
        reply = self.login_user()
        token = reply['token']
        report = {
            "comment": "No comment",
            "createdby": 1,
            "createdon": "Thu, 13 Dec 2018 08:33:24 GMT",
            "image": "img.jpg",
            "inctype": "intervention",
            "location": [12112.01,12122.454],
            "status": "under_investigation",
            "video": "video.avi"
        }
        response = self.tester.post(
            '/api/v1/interventions', content_type='application/json',
            data = json.dumps(report), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
     
        self.assertIn("intervention has been created successfuly", reply['message'])
        self.assertEqual(response.status_code, 201)
        update_status = { "status": "rejected"}
        response = self.tester.patch(
            '/api/v1/interventions/12/status', content_type='application/json',
            data = json.dumps(update_status), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
        self.assertIn(reply["error"], "Please intervention does not exit or check your id")
        self.assertEqual(response.status_code, 404)

    def test_test_delete(self):
        reply = self.login_user()
        token = reply['token']
        report = {
            "comment": "No comment",
            "createdby": 1,
            "createdon": "Thu, 13 Dec 2018 08:33:24 GMT",
            "image": "img.jpg",
            "inctype": "intervention",
            "location": [12112.01,12122.454],
            "status": "delivered",
            "video": "video.avi"
        }
        response = self.tester.post(
            '/api/v1/interventions', content_type='application/json',
            data = json.dumps(report), headers={'Authorization': f'Bearer {token}'}
        )
        reply = json.loads(response.data.decode())
        self.assertIn("intervention has been created successfuly", reply['message'])
        self.assertEqual(response.status_code, 201)
        response = self.tester.delete(
            '/api/v1/intervention/1', content_type='application/json', headers={'Authorization': f'Bearer {token}'}
        )
        self.assertEqual(response.status_code, 200)


    def tearDown(self):
        self.db.drop_table('interventions')

