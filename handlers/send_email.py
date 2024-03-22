import json
import boto3
from botocore.exceptions import ClientError

def validate_data(data):
    required_fields = ['from_address', 'to_address', 'subject', 'body']
    if not all(field in data and data[field] for field in required_fields):
        missing = [field for field in required_fields if field not in data or not data[field]]
        raise ValueError(f"Missing required parameters: {', '.join(missing)}")

def send_email_via_ses(from_address, to_address, subject, body, region='us-east-1'):
    """
    Sends an email using Amazon SES.
    
    :param from_address: Email address of the sender
    :param to_address: Email address of the recipient
    :param subject: Subject of the email
    :param body: Body of the email
    :param region: AWS region for the SES service
    :return: SES send_email response
    """
    client = boto3.client('ses', region_name=region)
    response = client.send_email(
        Destination={
            'ToAddresses': [to_address],
        },
        Message={
            'Body': {
                'Text': {
                    'Charset': "UTF-8",
                    'Data': body,
                },
            },
            'Subject': {
                'Charset': "UTF-8",
                'Data': subject,
            },
        },
        Source=from_address,
    )
    return response

def send_email(request, context):
    try:
        data = request['body']
        validate_data(data)
        
        # Send the email via SES
        response = send_email_via_ses(
            from_address=data['from_address'],
            to_address=data['to_address'],
            subject=data['subject'],
            body=data['body']
        )
        
        # Provide a response
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True,
            },
            "body": json.dumps({"message": "Email sent successfully", "response": response})
        }

    except ClientError as e:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True,
            },
            "body": json.dumps({"error": e.response['Error']['Message']})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True,
            },
            "body": json.dumps({"error": str(e)})
        }
