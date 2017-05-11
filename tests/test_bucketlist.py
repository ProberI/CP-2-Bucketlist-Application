import unittest
import json
from app import app, EnvironmentName, databases


class BucketlistTestCases(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        EnvironmentName('TestingConfig')
        databases.create_all()

    def tearDown(self):
        databases.session.remove()
        databases.drop_all()

    def test_register_status_code(self):
        payload = json.dumps({'username': 'Paul', 'password': 'XXC'})
        response = self.app.post('/bucketlist/api/v1/register', data=payload)
        self.assertEqual(response.status_code, 201)

    def test_register_status_message(self):
        payload = json.dumps({'username': 'Paul', 'password': 'XXC'})
        response = self.app.post('/bucketlist/api/v1/register', data=payload)
        self.assertIn('Successfully registered Paul', response.data.decode('utf-8'))

    def test_register_without_username(self):
        payload = json.dumps({'username': '', 'password': 'XXC'})
        response = self.app.post('/bucketlist/api/v1/register', data=payload)
        self.assertIn('Registration cannot be completed without username',
                      response.data.decode('utf-8'))

    def test_register_with_special_characters(self):
        payload = json.dumps({'username': 'ˆ&Paul', 'password': 'XXC'})
        response = self.app.post('/bucketlist/api/v1/register', data=payload)
        self.assertIn('Name cannot have special characters',
                      response.data.decode('utf-8'))
        # self.assertEqual(response.status_code, )

    def test_register_with_existing_username(self):
        payload = json.dumps({'username': 'ˆ&Paul', 'password': 'XXC'})
        response = self.app.post('/bucketlist/api/v1/register', data=payload)
        response = self.app.post('/bucketlist/api/v1/register', data=payload)
        self.assertIn('Username already exists', response.data.decode('utf-8'))

    def test_register_with_short_password(self):
        payload = json.dumps({'username': 'ˆ&Paul', 'password': 'X'})
        response = self.app.post('/bucketlist/api/v1/register', data=payload)
        self.assertIn('Password too short',
                      response.data.decode('utf-8'))
