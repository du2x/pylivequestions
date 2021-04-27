from business.question import get_active_question_in_room
from lambda_utils import get_url_parameter_from_event, create_cors_enabled_response


def handler(event, context):
    name = get_url_parameter_from_event(event)
    q = get_active_question_in_room(name)
    if q:
        return create_cors_enabled_response(q)
    else:
        return create_cors_enabled_response('')

