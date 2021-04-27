from datetime import datetime
from boto3.dynamodb.conditions import Key
from data.repository import Repository
from domain.model import Question, Room
from slugify import slugify


class RoomRepository(Repository):

    def create(self, room: Room):
        uuid = slugify(room.name)
        if self.get_by_name(room.name):
            return None
        self.table.put_item(
            Item={
                'PK': 'ROOM',
                'SK': 'ROOM#' + uuid,
                'uuid': uuid,
                'name': room.name,
                'room_state': room.state,  # state is reserved (??)
                'room_owner': room.owner,  # owner is reserved (??)
                'createdAt': datetime.now().isoformat()
            }
        )
        return uuid

    def get_by_name(self, name: str):
        response = self.table.query(KeyConditionExpression=Key('PK').eq('ROOM') & Key('SK').eq('ROOM#' + name))
        if len(response['Items']) == 0:
            return None
        r = response['Items'][0]
        return self.data_to_room(r)

    def get_all(self):
        response = self.table.query(KeyConditionExpression=Key('PK').eq('ROOM'))
        items = response['Items']
        return [self.data_to_room(r) for r in items]

    def include_question(self, room_name: str, question_uuid: str, question: Question):
        question.pickedAt = datetime.now().isoformat()
        response = self.table.put_item(
            Item={
                'PK': 'QUESTION#ROOM#' + room_name,
                'SK': question.pickedAt,
                'text': question.text,
                'uuid': question_uuid,
                'pickedAt': question.pickedAt,
                'options': [{'text': option['text'], 'correct': option['correct'],
                             'post_text': option['post_text']} for option in question.options]
            }
        )
        return response

    def update_room_state(self, room_id: str, room_state: str):
        response = self.table.update_item(
            Key={
                'PK': 'ROOM',
                'SK': 'ROOM#' + room_id
            },
            UpdateExpression="set room_state=:s",
            ExpressionAttributeValues={
                ':s': room_state
            },
            ReturnValues="UPDATED_NEW"
        )
        return response

    def data_to_room(self, data):
        r = Room(data['name'], data['room_owner'], data['room_state'])
        r.uuid = data['uuid']
        return r
