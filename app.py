import os

import boto3
from flask import Flask, jsonify, make_response, request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)


dynamodb_client = boto3.client('dynamodb')

if os.environ.get('IS_OFFLINE'):
    dynamodb_client = boto3.client(
        'dynamodb', region_name='localhost', endpoint_url='http://localhost:8000'
    )


USERS_TABLE = os.environ['USERS_TABLE']

def create_smtp_client(smtp_server, smtp_port, smtp_username, smtp_password):
    smtp_client = smtplib.SMTP(smtp_server, smtp_port)
    smtp_client.starttls()
    smtp_client.login(smtp_username, smtp_password)
    return smtp_client

def construct_email(from_address, to_address, subject, body):
    message = MIMEMultipart()
    message['From'] = from_address
    message['To'] = to_address
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))
    return message

@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        data = request.json
        from_address = data.get('from_address')
        to_address = data.get('to_address')
        subject = data.get('subject')
        body = data.get('body')
        smtp_server = data.get('smtp_server')
        smtp_port = data.get('smtp_port')
        smtp_username = data.get('smtp_username')
        smtp_password = data.get('smtp_password')

        if not all([from_address, to_address, subject, body, smtp_server, smtp_port, smtp_username, smtp_password]):
            return jsonify({'error': 'Missing required parameters'}), 400

        smtp_client = create_smtp_client(smtp_server, smtp_port, smtp_username, smtp_password)
        message = construct_email(from_address, to_address, subject, body)

        smtp_client.send_message(message)
        smtp_client.quit()

        return jsonify({'message': 'Email sent successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/users/<string:user_id>')
def get_user(user_id):
    result = dynamodb_client.get_item(
        TableName=USERS_TABLE, Key={'userId': {'S': user_id}}
    )
    item = result.get('Item')
    if not item:
        return jsonify({'error': 'Could not find user with provided "userId"'}), 404

    return jsonify(
        {'userId': item.get('userId').get('S'), 'name': item.get('name').get('S')}
    )


@app.route('/users', methods=['POST'])
def create_user():
    user_id = request.json.get('userId')
    name = request.json.get('name')
    if not user_id or not name:
        return jsonify({'error': 'Please provide both "userId" and "name"'}), 400

    dynamodb_client.put_item(
        TableName=USERS_TABLE, Item={'userId': {'S': user_id}, 'name': {'S': name}}
    )

    return jsonify({'userId': user_id, 'name': name})


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)
