import unittest
import json
from app import app

class TestSendEmailEndpoint(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_send_email_success(self):
        data = {
            'from_address': 'sender@example.com',
            'to_address': 'recipient@example.com',
            'subject': 'Test Subject',
            'body': 'Test Body',
            'smtp_server': 'smtp.example.com',
            'smtp_port': 587,
            'smtp_username': 'username',
            'smtp_password': 'password'
        }
        response = self.app.post('/send_email', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {'message': 'Email sent successfully'})

    def test_missing_parameters(self):
        data = {
            'from_address': 'sender@example.com',
            'to_address': 'recipient@example.com',
            'subject': 'Test Subject',
            # Missing 'body', 'smtp_server', 'smtp_port', 'smtp_username', 'smtp_password'
        }
        response = self.app.post('/send_email', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data), {'error': 'Missing required parameters'})

if __name__ == '__main__':
    unittest.main()
