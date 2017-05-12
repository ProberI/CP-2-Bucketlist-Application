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

    def test_register_with_unknown_route(self):
        payload = json.dumps({'username': 'Paul', 'password': 'XXCuywuyuwe'})
        response = self.app.post('/bucketlist/api/v1/registe', data=payload)
        self.assertEqual(response.status_code, 404)

    def test_register_status_code(self):
        payload = json.dumps({'username': 'Paul', 'password': 'XXChjdbsbds'})
        response = self.app.post('/bucketlist/api/v1/register', data=payload)
        self.assertEqual(response.status_code, 201)

    def test_register_status_message(self):
        payload = json.dumps({'username': 'Paul', 'password': 'XXCjkdsjdbsjbds'})
        response = self.app.post('/bucketlist/api/v1/register', data=payload)
        self.assertIn('Successfully registered Paul', response.data.decode('utf-8'))

    def test_register_without_username(self):
        payload = json.dumps({'username': '', 'password': 'XXCbjsdjkdsb'})
        response = self.app.post('/bucketlist/api/v1/register', data=payload)
        self.assertIn('Username cannot be blank', response.data.decode('utf-8'))

    def test_register_with_special_characters(self):
        payload = json.dumps({'username': 'ˆ&Paul', 'password': 'XXCkbsbdk'})
        response = self.app.post('/bucketlist/api/v1/register', data=payload)
        self.assertIn('Username cannot contain special characters',
                      response.data.decode('utf-8'))
        # self.assertEqual(response.status_code, )

    def test_register_with_existing_username(self):
        payload = json.dumps({'username': 'Paul', 'password': 'XXCsbdjjskds'})
        response = self.app.post('/bucketlist/api/v1/register', data=payload)
        response = self.app.post('/bucketlist/api/v1/register', data=payload)
        self.assertIn('This username is already in use', response.data.decode('utf-8'))

    def test_register_with_short_password(self):
        payload = json.dumps({'username': 'Paul', 'password': 'X'})
        response = self.app.post('/bucketlist/api/v1/register', data=payload)
        self.assertIn('Password should be more than 5 characters',
                      response.data.decode('utf-8'))

    def test_Login(self):
        payload = json.dumps({'username': 'Paul', 'password': 'Upendo'})
        self.app.post('/bucketlist/api/v1/register', data=payload)
        response = self.app.post('/bucketlist/api/v1/login', data=payload)
        self.assertIn('Successfully Logged in',
                      response.data.decode('utf-8'))

    def test_Login_with_invalid_credentials(self):
        payload = json.dumps({'username': 'Pau', 'password': 'Upendo'})
        response = self.app.post('/bucketlist/api/v1/login', data=payload)
        self.assertIn('Invalid credentials', response.data.decode('utf-8'))

    def test_login_with_special_characters_in_username(self):
        payload = json.dumps({'username': 'Pauˆ', 'password': 'Nada'})
        response = self.app.post('/bucketlist/api/v1/login', data=payload)
        self.assertEqual(response.status_code, 400)

    def test_login_with_blank_password(self):
        payload = json.dumps({'username': 'Pau', 'password': ''})
        response = self.app.post('/bucketlist/api/v1/login', data=payload)
        self.assertTrue(response.status_code == 400)
