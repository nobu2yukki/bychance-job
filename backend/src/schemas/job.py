from pydantic import BaseModel


class Job(BaseModel):
    id: int
    job: str
    place: str
    salary: str
