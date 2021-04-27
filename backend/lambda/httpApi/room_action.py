from pprint import pprint
from lambda_utils import parse_body_from_event, get_username_from_event, get_url_parameter_from_event, \
    create_cors_enabled_response
from business.room import include_question_to_room, close_question_to_room, close_room
from exceptions import AuthError


def handler(event, context):
    pprint(event)
    data = parse_body_from_event(event)
    data['username'] = get_username_from_event(event)
    name = get_url_parameter_from_event(event)
    try:
        if data['action'] == 'pick':
            include_question_to_room(name, data['question_uuid'], data['username'])
        elif data['action'] == 'close-question':
            close_question_to_room(name, data['username'])
        elif data['action'] == 'close-room':
            close_room(name, data['username'])
    except AuthError as err:
        return create_cors_enabled_response('Could not update room.', err.status_code)
    return create_cors_enabled_response(name + ' updated.')
