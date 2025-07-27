from pydantic import BaseModel


class JobCategory(BaseModel):
    parent: str
    child: str


class Job(BaseModel):
    id: int
    company_name: str
    page_url: str
    image_url: str
    place: str
    salary: str
    description: str
    category: JobCategory
    work_style: list[str]
    audience: list[str]
