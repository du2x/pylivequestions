from exceptions import AuthError
from business.question import get_question_by_uuid
from data.question import QuestionRepository
from data.room import RoomRepository
from data.connection import ConnectionRepository
from domain.model import Room, RoomState

conn_repo = ConnectionRepository()
rrepo = RoomRepository()
qrepo = QuestionRepository()


def create_room(data):
    rid = rrepo.create(Room(**data))
    return rid


def get_room_by_name(name: str):
    return rrepo.get_by_name(name)


def include_question_to_room(room_name: str, question_uuid: str, user: str):
    r = rrepo.get_by_name(room_name)
    if r.owner != user:
        raise AuthError('you can not update this room', 403)
    q = get_question_by_uuid(question_uuid)
    rrepo.include_question(room_name, question_uuid, q)
    rrepo.update_room_state(room_name, RoomState.QUESTION_OPENED.value)


def close_question_to_room(room_name: str, user: str):
    r = rrepo.get_by_name(room_name)
    if r.owner != user:
        raise AuthError('you can not update this room', 403)
    rrepo.update_room_state(room_name, RoomState.QUESTION_CLOSED.value)


def close_room(room_id: str, user: str):
    r = rrepo.get_by_name(room_id)
    if r.owner != user:
        raise AuthError('you can not update this room', 403)
    conn_repo.delete_connections_by_room_id(room_id)
    rrepo.update_room_state(room_id, RoomState.ROOM_CLOSED.value)


def get_all_rooms():
    return rrepo.get_all()
