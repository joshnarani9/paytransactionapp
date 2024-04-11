import unittest
import json
from run import app

class TestAPI(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_match_users_endpoint(self):
        # Test the /api/match_users endpoint
        payload = {'transaction_id': 'mkcUo5Z7'}
        response = self.app.post('/api/match_users', json=payload)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('users', data)
        self.assertIn('total_number_of_matches', data)

    def test_find_similar_transactions_endpoint(self):
        # Test the /api/match_txns endpoint
        query_string = {'description': 'example_description'}
        response = self.app.get('/api/match_txns', query_string=query_string)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('transactions', data)
        self.assertIn('total_number_of_tokens_used', data)

if __name__ == '__main__':
    unittest.main()
