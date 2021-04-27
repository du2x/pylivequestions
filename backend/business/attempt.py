from exceptions import AuthError
from domain.model import Question, Attempt
from business.question import get_active_question_in_room
from data.room import RoomRepository
from data.attempt import AttemptRepository
from domain.model import RoomState

arepo = AttemptRepository()
rrepo = RoomRepository()


def make_attempt(data):
    room = rrepo.get_by_name(data['room_id'])
    if room.state != RoomState.QUESTION_OPENED.value:
        return 0  # TODO: throw exception and handle it on lambda
    arepo.create(Attempt(**data))
    return 1


def get_attempt_result(room_name, question_uuid, answer):
    q = get_active_question_in_room(room_name)
    if q['uuid'] != question_uuid:
        return None
    return q.proccess_attemp(answer)


def get_attempts_against_question_and_room(question_uuid: str, room_id: str):
    return arepo.get_by_question_uuid_and_room_id(question_uuid, room_id)
