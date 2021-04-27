from domain.model import Attempt
from boto3.dynamodb.conditions import Key
from data.repository import Repository


class AttemptRepository(Repository):

    def create(self, attempt: Attempt):
        response = self.table.put_item(
            Item={
                'PK': 'ATTEMPT#QUESTION#' + attempt.question_uuid,
                'SK': 'ROOM#' + attempt.room_id + '#USER#' + attempt.username,
                'question_uuid': attempt.question_uuid,
                'username': attempt.username,
                'room_id': attempt.room_id,
                'answer': attempt.answer
            }
        )
        return response

    def get_by_question_uuid_and_room_id(self, question_uuid: str, room_id: str):
        response = self.table.query(
            KeyConditionExpression=Key('PK').eq('ATTEMPT#QUESTION#' + question_uuid) & Key('SK').begins_with(
                'ROOM#' + room_id))
        ats = [self.data_to_attempt(item) for item in response['Items']]
        return ats

    def data_to_attempt(self, data):
        return Attempt(data['username'], data['question_uuid'], data['room_id'], data['answer'])
