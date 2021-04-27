from data.repository import Repository
from datetime import datetime
from boto3.dynamodb.conditions import Key

from domain.model import WSConnection


class ConnectionRepository(Repository):

    def create(self, connection: WSConnection):
        response = self.table.put_item(
            Item={
                'PK': 'CONNECTION#ROOM#' + connection.room_id,
                'SK': 'CONNECTION#' + connection.connection_id,
                'connection_id': connection.connection_id,  # there will be a gsi in this field
                'username': connection.username,
                'created': datetime.now().isoformat()
            }
        )
        return response

    def get_by_room_id(self, room_id: str, raw=False):
        response = self.table.query(
            KeyConditionExpression=Key('PK').eq('CONNECTION#ROOM#' + room_id) & Key('SK').begins_with('CONNECTION#'))
        if len(response['Items']) == 0:
            return None
        data = response['Items']
        if(raw):
            return data
        return [WSConnection(connection_id=item['connection_id'], room_id=item['PK'].split('#')[2],
                             username=item['username']) for item in data]

    def delete(self, room_id: str, connection_id: str):
        response = self.table.delete_item(IndexName='connection_id',
                                          KeyConditionExpression=Key('PK').eq('CONNECTION#ROOM#' + room_id)
                                                                         & Key('SK').eq('CONNECTION#' + connection_id))
        return response

    def delete_connections_by_room_id(self, room_id: str):
        items = self.get_by_room_id(room_id, True)
        for item in items:
            self.table.delete_item(
                Key={'PK': item['PK'],
                     'SK': item['SK']}
            )
            return 1
