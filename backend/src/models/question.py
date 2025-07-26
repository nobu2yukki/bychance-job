from pydantic import BaseModel


class AnswerPayload(BaseModel):
    answers: dict[int, str | list[str]]
