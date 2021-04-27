from pprint import pprint

import json
import logging

import config
from business.question import get_question_by_uuid, get_active_question_in_room
from business.room import get_room_by_name
from business.attempt import get_attempts_against_question_and_room
from business.connection import get_connections_by_room

import boto3
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

logger = logging.getLogger()
logger.setLevel(logging.INFO)
patch_all()

apig_management_client = boto3.client(
    'apigatewaymanagementapi', endpoint_url=f'https://{config.WS_DOMAIN}/{config.STAGE}')


def handler(event, context):
    try:
        for record in event['Records']:
            pprint(record)
            if record['eventName'] == 'MODIFY' and record['dynamodb']['Keys']['PK']['S'] == 'ROOM':
                print('will notify attempter')
                room_id = record['dynamodb']['Keys']['SK']['S'].split('#')[1]
                question_active_response = get_active_question_in_room(room_id)
                question = get_question_by_uuid(question_active_response['uuid'])
                connections = get_connections_by_room(room_id)
                attempts = get_attempts_against_question_and_room(question.uuid, room_id)
                for connection in connections:
                    c_attempt = next(iter([a for a in attempts if a.username == connection.username]), None)
                    if c_attempt:
                        result = question.proccess_attempt(c_attempt.answer)
                        try:
                            send_response = apig_management_client.post_to_connection(
                                Data=json.dumps(result.__dict__), ConnectionId=connection.connection_id)
                            logger.info(
                                "Posted message to connection %s, got response %s.",
                                connection.connection_id, send_response)
                        except Exception as err:
                            logger.error(err)    #TODO: if GoneException delete connection
            if record['eventName'] == 'INSERT' and record['dynamodb']['Keys']['PK']['S'].startswith('QUESTION#ROOM#'):
                print('will notify new question')
                room_id = record['dynamodb']['Keys']['PK']['S'].split('#')[2]
                connections = get_connections_by_room(room_id)
                for connection in connections:
                    try:
                        send_response = apig_management_client.post_to_connection(
                            Data='new question', ConnectionId=connection.connection_id)
                        logger.info(
                            "Posted message to connection %s, got response %s.",
                            connection.connection_id, send_response)
                    except Exception as err:
                        logger.error(err)  #TODO: if GoneException delete connection

            if record['eventName'] in ['INSERT', 'MODIFY'] and record['dynamodb']['Keys']['PK']['S'].startswith('ATTEMPT'):
                print('will notify room owner')
                action = ''
                if record['eventName'] == 'INSERT':
                    action = 'answered'
                if record['eventName'] == 'MODIFY':
                    action = 'has change his/her answer to'
                room_id = record['dynamodb']['Keys']['SK']['S'].split('#')[1]
                room = get_room_by_name(room_id)
                connections = get_connections_by_room(room_id) # MAYBE NEW INDEX FOR FIND BY ROOM and username
                o_connections = [c for c in connections if c.username == room.owner]
                attempt_data = record['dynamodb']['NewImage']
                print('attempt data:')
                message = f"{attempt_data['username']['S']} {action} {attempt_data['answer']['S']}"
                for connection in o_connections:
                    try:
                        send_response = apig_management_client.post_to_connection(
                            Data=message, ConnectionId=connection.connection_id)
                        logger.info(
                            "Posted message to connection %s, got response %s.",
                            connection.connection_id, send_response)
                    except Exception as err:
                        logger.error(err)      #TODO: if GoneException delete connection

    except Exception as err:
        logger.error(err)
