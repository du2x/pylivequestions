import json

from business.room import get_all_rooms
from lambda_utils import create_cors_enabled_response


def handler(event, context):
    rs = get_all_rooms()
    message = [r.__dict__ for r in rs]
    return create_cors_enabled_response(message)

