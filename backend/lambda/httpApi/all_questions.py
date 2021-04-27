from business.question import get_all_questions
from lambda_utils import create_cors_enabled_response


def handler(event, context):
    qs = get_all_questions()
    message = [q.__dict__ for q in qs]
    return create_cors_enabled_response(message)

