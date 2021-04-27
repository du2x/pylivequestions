import uuid
from domain.model import RoomState, Question
from data.question import QuestionRepository
from data.room import RoomRepository

repo = QuestionRepository()
room_repo = RoomRepository()


def create_question(data):
    q = Question(**data)
    qid = uuid.uuid4().hex    
    return repo.create(qid, q)


def get_all_questions():
    return repo.get_all()


def get_active_question_in_room(room_uuid):    
    qs = repo.get_by_room_name(room_uuid)
    if not qs:
        return None
    room = room_repo.get_by_name(room_uuid)
    oqs = sorted(qs, key=lambda k: k.pickedAt)
    q = oqs[-1]  # active question will be always the last opened question in room
    if room.state == RoomState.QUESTION_OPENED.value:
        return {'text': q.text, 'uuid': q.uuid, 'options': q.ref_options(True), 'type': q.get_type}
    else:
        return {'text': q.text, 'uuid': q.uuid, 'options': q.ref_options(False), 'type': q.get_type}


def get_question_by_uuid(question_uuid):
    q = repo.get_by_uuid(question_uuid)
    return q
