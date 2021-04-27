from business.attempt import make_attempt
from lambda_utils import parse_body_from_event, get_username_from_event, create_cors_enabled_response


def handler(event, context):
    data = parse_body_from_event(event) # I dont know why, but this lambda is receiving the body not b64 encoded
    data['username'] = get_username_from_event(event)
    if data['answer'] == '':
        return create_cors_enabled_response('you have sent empty answer.')
    ret = make_attempt(data)
    if ret:
        return create_cors_enabled_response('attempt registered.')
    return create_cors_enabled_response('can not make attempt to this question anymore. (time is out!)', 201)