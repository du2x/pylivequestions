from business.connection import create_connection, delete_connection


def connection_handler(event, context):
    param = event.get('queryStringParameters', {'data': 'default,guest'}).get('data')
    param_data = param.split(',')
    conn_data = {'room_id': param_data[0],
            'username': param_data[1],
            'connection_id': event['requestContext']['connectionId']}
    create_connection(conn_data)
    return {'statusCode': 200}


def disconnection_handler(event, context):
    param = event.get('queryStringParameters', {'data': 'default,guest'}).get('data')
    param_data = param.split(',')
    delete_connection(param_data[0],event['requestContext']['connectionId'])
    return {'statusCode': 200}
