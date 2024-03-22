import json
import unittest
from unittest.mock import patch, MagicMock
from handlers.send_email import create_smtp_client, construct_email, validate_data, send_email  # Adjust the import path according to your project structure

class TestEmailFunctions(unittest.TestCase):

    @patch('handlers.send_email.smtplib.SMTP')
    def test_create_smtp_client_success(self, mock_smtp):
        smtp_server = 'smtp.example.com'
        smtp_port = 587
        smtp_username = 'user@example.com'
        smtp_password = 'password'
        create_smtp_client(smtp_server, smtp_port, smtp_username, smtp_password)
        mock_smtp.assert_called_with(smtp_server, smtp_port)
        mock_smtp.return_value.starttls.assert_called_once()
        mock_smtp.return_value.login.assert_called_with(smtp_username, smtp_password)

    def test_construct_email(self):
        from_address = 'from@example.com'
        to_address = 'to@example.com'
        subject = 'Test Subject'
        body = 'Test Body'
        message = construct_email(from_address, to_address, subject, body)
        self.assertEqual(message['From'], from_address)
        self.assertEqual(message['To'], to_address)
        self.assertEqual(message['Subject'], subject)
        self.assertTrue(str(message).find(body) != -1)

    def test_validate_data_success(self):
        data = {
            'from_address': 'from@example.com',
            'to_address': 'to@example.com',
            'subject': 'Test Subject',
            'body': 'Test Body',
            'smtp_server': 'smtp.example.com',
            'smtp_port': 587,
            'smtp_username': 'user@example.com',
            'smtp_password': 'password'
        }
        # Should not raise an exception
        validate_data(data)

    def test_validate_data_failure(self):
        data = {
            'from_address': 'from@example.com'
            # Missing other required fields
        }
        with self.assertRaises(ValueError) as context:
            validate_data(data)
        self.assertTrue('Missing required parameters' in str(context.exception))

    @patch('handlers.send_email.create_smtp_client')
    @patch('handlers.send_email.construct_email')
    @patch('handlers.send_email.json.dumps')
    @patch('handlers.send_email.json.loads')
    def test_send_email(self, mock_loads, mock_dumps, mock_construct_email, mock_create_smtp_client):
        # Prepare the request mock
        request_body = {
            'from_address': 'from@example.com',
            'to_address': 'to@example.com',
            'subject': 'Test Subject',
            'body': 'Test Body',
            'smtp_server': 'smtp.example.com',
            'smtp_port': 587,
            'smtp_username': 'user@example.com',
            'smtp_password': 'password'
        }
        request = {'body': json.dumps(request_body)}
        mock_loads.return_value = request_body  # Simulate json.loads parsing JSON from the request body

        # Simulate the expected behavior of json.dumps
        mock_dumps.return_value = json.dumps({"message": "Email sent successfully"})

        context = {}
        response = send_email(request, context)

        # Check if the response body (after json.dumps mock is applied) contains the expected message
        expected_response_body = json.dumps({"message": "Email sent successfully"})
        self.assertEqual(response['body'], expected_response_body)

if __name__ == '__main__':
    unittest.main()
