import json

from business.attempt import get_attempts_against_question_and_room
from lambda_utils import create_cors_enabled_response, parse_body_from_event, get_username_from_event
from exceptions import AuthError


def handler(event, context):
    data = parse_body_from_event(event)
    room_id = data['room_id']
    question_uuid = data['question_uuid']
    user = get_username_from_event(event)
    try:
        attempts = get_attempts_against_question_and_room(question_uuid, room_id, user)
        return create_cors_enabled_response([{'username': a.username, 'answer': a.answer} for a in attempts])
    except AuthError as err:
        return create_cors_enabled_response(json.dumps(err), 403)
