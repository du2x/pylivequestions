from datetime import datetime
from pprint import pprint
from boto3.dynamodb.conditions import Key
from data.repository import Repository
from domain.model import Question


class QuestionRepository(Repository):

    def create(self, question_uuid: str, question: Question):
        question.created_at = datetime.now().isoformat()
        response = self.table.put_item(
            Item={
                'PK': 'QUESTION',
                'SK': 'QUESTION#' + question_uuid,
                'uuid': question_uuid,
                'text': question.text,
                'options': [{'text': option['text'], 'correct': option['correct'],
                             'post_text': option['post_text']} for option in question.options]
            }
        )
        return question_uuid

    def get_all(self):
        response = self.table.query(KeyConditionExpression=Key('PK').eq('QUESTION'))
        items = response['Items']
        return [self.data_to_question(r) for r in items]

    def get_by_uuid(self, question_uuid: str):
        response = self.table.query(
            KeyConditionExpression=Key('PK').eq('QUESTION') & Key('SK').eq('QUESTION#' + question_uuid))
        q = self.data_to_question(response['Items'][0])
        return q

    def get_by_room_name(self, room_name: str):
        response = self.table.query(KeyConditionExpression=Key('PK').eq('QUESTION#ROOM#' + room_name))
        qs = [self.data_to_question(item) for item in response['Items']]
        return qs

    def data_to_question(self, data):
        q = Question(data['text'], data['options'])
        q.uuid = data['uuid']
        if 'pickedAt' in data.keys():
            q.pickedAt = data['pickedAt']
        return q
