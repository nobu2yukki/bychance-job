from pydantic import BaseModel


# 質問の表示用
class Question(BaseModel):
    id: int
    question: str
    options: list[str]


# class ShowCondition(BaseModel):
#     condition: dict[str, str]


class InitialQuestionNoCondition(BaseModel):
    id: int
    type: str
    label: str
    options: list


class InitialQuestion(BaseModel):
    id: int
    type: str
    label: str
    options: list
    showcondition: dict


# 回答の送信用
class AnswerSubmission(BaseModel):
    answers: dict[int, str]


class AnswerInput(BaseModel):
    session_id: str
    question_id: int
    answer: str


class AnswerPayload(BaseModel):
    answers: dict[str, str | list[str]]
