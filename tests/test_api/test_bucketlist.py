import unittest
import json
from app import app, EnvironmentName, databases


class BucketlistTestCases(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()  # Send virtual requests to the application
        EnvironmentName('TestingConfig')
        databases.create_all()

    def tearDown(self):
        databases.session.remove()
        databases.drop_all()

    def test_create_bucketlist_with_empty_name(self):
        payload = json.dumps({'name': ''})  # Encode the payload arguments in json
        response = self.app.post('bucketlist/api/v1/bucketlist', data=payload)
        self.assertIn('Your Bucketlist needs a name/title to proceed.',
                      response.data.decode('utf-8'))

    def test_create_bucketlist(self):
        payload = json.dumps({'name': 'Before I kick the bucket.'})
        response = self.app.post('bucketlist/api/v1/bucketlist', data=payload)
        self.assertTrue(response.status_code == 201)
        self.assertIn('Success', response.data.decode('utf-8'))

    def test_get_bucketlist_while_empty(self):
        response = self.app.get('/bucketlist/api/v1/bucketlist')
        self.assertTrue(response.status_code == 200)
        self.assertIn('Ooops! You have not created any bucketlist yet',
                      response.data.decode('utf-8'))

    def test_get_Bucketlist(self):
        payload = json.dumps({'name': 'Before I kick the bucket.'})
        response = self.app.post('/bucketlist/api/v1/bucketlist', data=payload)
        response = self.app.get('/bucketlist/api/v1/bucketlist')
        self.assertEqual(response.status_code, 200)

    def test_get_bucketlist_by_id(self):
        payload = json.dumps({'name': 'Before I kick the bucket.'})
        response = self.app.post('bucketlist/api/v1/bucketlist', data=payload)
        response = self.app.get('/bucketlist/api/v1/bucketlist/1')
        self.assertEqual(response.status_code, 200)

    def test_get_bucketlist_with_invalid_id(self):
        payload = json.dumps({'name': 'Before I kick the bucket.'})
        response = self.app.post('bucketlist/api/v1/bucketlist', data=payload)
        response = self.app.get('/bucketlist/api/v1/bucketlist/20')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Ooops! Sorry this bucketlist does not exist.',
                      response.data.decode('utf-8'))

    def test_delete_bucketlist_with_invalid_id(self):
        payload = json.dumps({'name': 'Before I kick the bucket.'})
        response = self.app.post('bucketlist/api/v1/bucketlist', data=payload)
        response = self.app.delete('/bucketlist/api/v1/bucketlist/20')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Ooops! Sorry this bucketlist does not exist.',
                      response.data.decode('utf-8'))

    def test_delete_bucketlist(self):
        payload = json.dumps({'name': 'Before I kick the bucket.'})
        response = self.app.post('bucketlist/api/v1/bucketlist', data=payload)
        response = self.app.delete('/bucketlist/api/v1/bucketlist/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Bucketlist successfully deleted',
                      response.data.decode('utf-8'))

    def test_edit_bucketlist_with_invalid_id(self):
        payload = json.dumps({'name': 'Before I kick the bucket.'})
        response = self.app.post('bucketlist/api/v1/bucketlist', data=payload)
        response = self.app.put('/bucketlist/api/v1/bucketlist/2', data=payload)
        self.assertEqual(response.status_code, 404)
        self.assertIn('Ooops! Sorry this bucketlist does not exist.',
                      response.data.decode('utf-8'))

    def test_edit_bucketlist(self):
        payload = json.dumps({'name': 'Before I kick the bucket.'})
        response = self.app.post('bucketlist/api/v1/bucketlist', data=payload)
        payload = json.dumps({'name': 'Die before I do.'})
        response = self.app.put('/bucketlist/api/v1/bucketlist/1', data=payload)
        self.assertEqual(response.status_code, 201)

    def test_add_items(self):
        payload = json.dumps({'name': 'Before I kick the bucket.'})
        response = self.app.post('bucketlist/api/v1/bucketlist', data=payload)
        payload = json.dumps({'name': 'Go with bae on a cruise.'})
        response = self.app.post('bucketlist/api/v1/bucketlist/1/items', data=payload)
        self.assertEqual(response.status_code, 200)

    def test_add_items_with_invalid_bucket_id(self):
        payload = json.dumps({'name': 'Before I kick the bucket.'})
        response = self.app.post('bucketlist/api/v1/bucketlist', data=payload)
        payload = json.dumps({'name': 'Go with bae on a cruise.'})
        response = self.app.post('bucketlist/api/v1/bucketlist/10/items', data=payload)
        self.assertEqual(response.status_code, 404)

    def test_edit_items(self):
        payload = json.dumps({'name': 'Before I kick the bucket.'})
        response = self.app.post('bucketlist/api/v1/bucketlist', data=payload)
        payload = json.dumps({'name': 'Go with bae on a cruise.'})
        response = self.app.post('bucketlist/api/v1/bucketlist/1/items', data=payload)
        payload = json.dumps({'name': 'Go with bae on a cruise. If she agrees to marry me'})
        response = self.app.put('bucketlist/api/v1/bucketlist/1/items/1', data=payload)
        self.assertEqual(response.status_code, 200)

    def test_add_items_that_exist(self):
        payload = json.dumps({'name': 'Before I kick the bucket.'})
        response = self.app.post('bucketlist/api/v1/bucketlist', data=payload)
        payload = json.dumps({'name': 'Go with bae on a cruise.'})
        response = self.app.post('bucketlist/api/v1/bucketlist/1/items', data=payload)
        response = self.app.post('bucketlist/api/v1/bucketlist/1/items', data=payload)
        self.assertIn('Ooops! Sorry, this particular item already exists.',
                      response.data.decode('utf-8'))

    def test_edit_items_that_dont_exist(self):
        payload = json.dumps({'name': 'Before I kick the bucket.'})
        response = self.app.post('bucketlist/api/v1/bucketlist', data=payload)
        payload = json.dumps({'name': 'Go with bae on a cruise. If she agrees to marry me'})
        response = self.app.put('bucketlist/api/v1/bucketlist/1/items/1', data=payload)
        self.assertIn('Ooops! The item_id does not exist.', response.data.decode('utf-8'))
        self.assertTrue(response.status_code == 404)

    def test_delete_bucketlist(self):
        payload = json.dumps({'name': 'Before I kick the bucket.'})
        response = self.app.post('bucketlist/api/v1/bucketlist', data=payload)
        response = self.app.delete('bucketlist/api/v1/bucketlist/1', data=payload)
        self.assertTrue(response.status_code == 200)

    def test_delete_items(self):
        payload = json.dumps({'name': 'Before I kick the bucket.'})
        response = self.app.post('bucketlist/api/v1/bucketlist', data=payload)
        payload = json.dumps({'name': 'Go with bae on a cruise. If she agrees to marry me'})
        response = self.app.post('bucketlist/api/v1/bucketlist/1/items', data=payload)
        response = self.app.delete('bucketlist/api/v1/bucketlist/1/items/1', data=payload)
        self.assertTrue(response.status_code == 200)

    def test_delete_items_with_invalid_bucketlist_id(self):
        payload = json.dumps({'name': 'Before I kick the bucket.'})
        response = self.app.post('bucketlist/api/v1/bucketlist', data=payload)
        payload = json.dumps({'name': 'Go with bae on a cruise. If she agrees to marry me'})
        response = self.app.post('bucketlist/api/v1/bucketlist/1/items', data=payload)
        response = self.app.delete('bucketlist/api/v1/bucketlist/10/items/1', data=payload)
        self.assertTrue(response.status_code == 404)

    def test_delete_items_with_invalid_items_id(self):
        payload = json.dumps({'name': 'Before I kick the bucket.'})
        response = self.app.post('bucketlist/api/v1/bucketlist', data=payload)
        payload = json.dumps({'name': 'Go with bae on a cruise. If she agrees to marry me'})
        response = self.app.post('bucketlist/api/v1/bucketlist/1/items', data=payload)
        response = self.app.delete('bucketlist/api/v1/bucketlist/1/items/15', data=payload)
        self.assertTrue(response.status_code == 404)
