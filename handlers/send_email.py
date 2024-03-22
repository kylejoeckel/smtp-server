from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import smtplib

def create_smtp_client(smtp_server, smtp_port, smtp_username, smtp_password):
    try:
        smtp_client = smtplib.SMTP(smtp_server, smtp_port)
        smtp_client.starttls()  # Upgrade the connection to SSL/TLS
        smtp_client.login(smtp_username, smtp_password)
        return smtp_client
    except Exception as e:
        raise ConnectionError(f"Failed to connect and log in to SMTP server: {e}")

def construct_email(from_address, to_address, subject, body):
    message = MIMEMultipart()
    message['From'] = from_address
    message['To'] = to_address
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))
    return message

def validate_data(data):
    required_fields = ['from_address', 'to_address', 'subject', 'body', 'smtp_server', 'smtp_port', 'smtp_username', 'smtp_password']
    if not all(field in data and data[field] for field in required_fields):
        missing = [field for field in required_fields if field not in data or not data[field]]
        raise ValueError(f"Missing required parameters: {', '.join(missing)}")

def send_email(request, context):
    try:
        data = json.loads(request['body'])
        validate_data(data)
        
        smtp_client = create_smtp_client(data['smtp_server'], data['smtp_port'], data['smtp_username'], data['smtp_password'])
        message = construct_email(data['from_address'], data['to_address'], data['subject'], data['body'])

        smtp_client.send_message(message)
        smtp_client.quit()

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({"message": "Email sent succesfully"})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({'error': str(e)})
        }
