from pydantic import BaseModel


class SwipeResult(BaseModel):
    session_id: str
    good: list[int]
    bad: list[int]
