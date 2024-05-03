from django.test import TestCase, Client
import json

class ViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

         # Add a test user
        data = {'username': 'Test', 'password': 'Test'}
        self.client.post('/myapp/add_user/', json.dumps(data), content_type='application/json')
        
        # Add a test reservation
        data = {'username': 'Test', 'slot_id': 50, 'expiry_hours': 2}
        self.client.post('/myapp/add_reservation/', json.dumps(data), content_type='application/json')

    def test_add_comment(self):
        data = {'comment': 'Test Comment', 'slot_id': 1}
        response = self.client.post('/myapp/add_comment/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        data = {'comment': 'Test Comment', 'slot_id': 100}
        response = self.client.post('/myapp/add_comment/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 403)


    def test_get_comment(self):
        response = self.client.get(f'/myapp/get_comments/?slot_id=50', content_type='application/json')
        self.assertEqual(response.status_code, 200)



    def test_get_available_locations(self):
        #Testing condition=all
        #Normally it's 50, but 1 slot is reserved for the setUp so should be 49
        response = self.client.get('/myapp/get_available_locations/', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['available_locations']), 49)

        #Testing condition=outer
        #Normally it's 30, but 1 slot is reserved for the setUp so should be 29
        response = self.client.get('/myapp/get_available_locations/?condition=outer', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['available_locations']), 29)

        #Testing condition=inner
        response = self.client.get('/myapp/get_available_locations/?condition=inner', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['available_locations']), 20)
    
    def test_slot_type(self):
        data = {'slot_id': 1}
        response = self.client.get('/myapp/slot_type/', data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'slot type is ': 'inner'})

        data = {'slot_id': 100}
        response = self.client.get('/myapp/slot_type/', data, content_type='application/json')
        self.assertEqual(response.status_code, 403)


    def test_authenticate_user(self):
        response = self.client.get('/myapp/authenticate_user/?username=Test&password=Test')
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get('/myapp/authenticate_user/?username=bad&password=bad')
        self.assertEqual(response.status_code, 403)
        
    def test_add_user(self):
        data = {'username': 'InTest', 'password': 'InTest'}
        response = self.client.post('/myapp/add_user/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'User added successfully'})

        response = self.client.post('/myapp/add_user/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_add_reservation(self):
        data = {'username': 'Test', 'slot_id': 1, 'expiry_hours': 2}
        response = self.client.post('/myapp/add_reservation/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Reservation added successfully'})

        response = self.client.post('/myapp/add_reservation/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {'error': 'Slot is already booked'})
    
    def test_get_your_reservations(self):
        response = self.client.get('/myapp/get_your_reservations/?username=Test')
        self.assertEqual(response.status_code, 200)

    def test_remove_reservation(self):
        data = {'slot_id': 50}
        response = self.client.delete('/myapp/remove_reservation/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Reservation removed successfully'})

        response = self.client.delete('/myapp/remove_reservation/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 403)
