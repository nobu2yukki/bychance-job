from pydantic import BaseModel


# 質問の表示用
class Question(BaseModel):
    id: int
    question: str
    options: list[str]


# 回答の送信用
class AnswerSubmission(BaseModel):
    answers: dict[int, str]


class AnswerInput(BaseModel):
    session_id: str
    question_id: int
    answer: str
