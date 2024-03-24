import json
import unittest
from unittest.mock import patch, MagicMock
from handlers.send_email import validate_data, send_email  # Adjust the import path according to your project structure

class TestEmailFunctions(unittest.TestCase):

    def test_validate_data_success(self):
        data = {
            'from_address': 'from@example.com',
            'to_address': 'to@example.com',
            'subject': 'Test Subject',
            'body': 'Test Body'
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

    @patch('handlers.send_email.boto3.client')
    def test_send_email(self, mock_boto3_client):
        # Mock the boto3 SES client response
        mock_send_email_response = {'MessageId': '1234'}
        mock_boto3_client.return_value.send_email.return_value = mock_send_email_response

        # Prepare the request mock
        request_body = {
            'from_address': 'from@example.com',
            'to_address': 'to@example.com',
            'subject': 'Test Subject',
            'body': 'Test Body'
        }
        request = {'body': request_body}  # Assuming body is already a dict for simplicity

        context = {}
        response = send_email(request, context)

        # Check if SES send_email was called
        mock_boto3_client.return_value.send_email.assert_called_once()

        # Check if the response contains the expected message
        expected_response_body = json.dumps({"message": "Email sent successfully", "response": mock_send_email_response})
        self.assertEqual(response['body'], expected_response_body)

        # Verify the status code of a successful response
        self.assertEqual(response['statusCode'], 200)

if __name__ == '__main__':
    unittest.main()
