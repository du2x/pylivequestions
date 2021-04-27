import json
import base64


def create_cors_enabled_response(message, status_code=200):
    headers = {
        # Required for CORS support to work
        'Access-Control-Allow-Origin': '*',
        # Required for cookies, authorization headers with HTTPS
        'Access-Control-Allow-Credentials': True
    }
    return create_aws_lambda_response(status_code, {'message': message}, headers)


def create_aws_lambda_response(status_code, message, headers):
    return {
        'statusCode': status_code,
        'headers': headers,
        'body': json.dumps(message)
    }


def parse_body_from_event(event):
    data = dict()
    try:
        data = json.loads(base64.b64decode(event['body']))
    except Exception as e:
        data = json.loads(event['body'])
    return data


def get_username_from_event(event):
    return event['requestContext']['authorizer']['jwt']['claims']['sub']


def get_url_parameter_from_event(event):
    return event['rawPath'].split('/')[-1]