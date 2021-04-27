from business.room import create_room
from lambda_utils import create_cors_enabled_response, parse_body_from_event, get_username_from_event


def handler(event, context):
    data = parse_body_from_event(event)
    data['owner'] = get_username_from_event(event)
    rid = create_room(data)
    return create_cors_enabled_response(rid)
