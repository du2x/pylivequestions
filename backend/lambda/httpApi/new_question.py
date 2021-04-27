from business.question import create_question
from lambda_utils import create_cors_enabled_response, parse_body_from_event


def handler(event, context):
    data = parse_body_from_event(event)
    qid = create_question(data)
    return create_cors_enabled_response(qid)
