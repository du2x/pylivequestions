from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from enum import Enum


class QuestionType(Enum):
    DISCURSIVE = 'discursive'
    SINGLEANSWER = 'single_answer'
    MULTIPLEANSWER = 'multiple_answer'


class RoomState(Enum):
    NO_QUESTION = 'no_question'  # OPENED
    QUESTION_OPENED = 'question_opened'  # OPENED
    QUESTION_CLOSED = 'question_closed'  # OPENED
    ROOM_CLOSED = 'room_closed'  # CLOSED


@dataclass
class Question:
    text: str
    options: Optional[List]
    pickedAt: datetime = None

    def proccess_attempt(self, answer: str):
        if self.get_type != QuestionType.DISCURSIVE:
            answer_spt = answer.split(',')
            correct_options = [self.options.index(option) for option in self.options if option['correct']]
            marked_correct = [{'ref': int(option), 'feedback': self.options[int(option)]['post_text']} for option in
                              answer_spt if int(option) in correct_options]
            unmarked_correct = [{'ref': option, 'feedback': self.options[option]['post_text']} for option in
                                correct_options if str(option) not in answer_spt]
            marked_incorrect = [{'ref': int(option), 'feedback': self.options[int(option)]['post_text']} for option in
                                answer_spt if int(option) not in correct_options]
            return AttemptResult(marked_correct, unmarked_correct, marked_incorrect)
        else:
            return AttemptResult(None, None, None)  # returns nothing

    @property
    def get_type(self):
        if len(self.options) == 0:
            return QuestionType.DISCURSIVE.value
        if len([option for option in self.options if option['correct']]) == 1:
            return QuestionType.SINGLEANSWER.value
        if len([option for option in self.options if option['correct']]) > 1:
            return QuestionType.MULTIPLEANSWER.value

    def ref_options(self, hide_answers=False):
        if hide_answers:
            return [{'ref': self.options.index(option), 'text': option['text']} for option in self.options]
        else:
            return [{'ref': self.options.index(option), 'text': option['text'], 'post_text': option['post_text'],
                     'correct': option['correct']} for option in self.options]


@dataclass(frozen=True)
class Attempt:
    username: str
    question_uuid: str
    room_id: str
    answer: str


@dataclass(frozen=True)
class AttemptResult:
    marked_correct: list
    unmarked_correct: list
    marked_incorrect: list

    @property
    def result_quotient(self) -> float:
        return len(self.marked_correct) / \
               (len(self.marked_correct) + len(self.unmarked_correct) + len(self.marked_incorrect))


@dataclass
class Room:
    name: str
    owner: str  # user
    state: str = RoomState.NO_QUESTION.value


@dataclass
class WSConnection:
    connection_id: str
    room_id: str
    username: str
