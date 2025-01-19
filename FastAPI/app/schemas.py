from pydantic import BaseModel


class CreateWorker(BaseModel):
    job_title: str
    firstname: str
    lastname: str
    age: int
    salary: float


class UpdateWorker(BaseModel):
    job_title: str
    lastname: str
    age: int
    salary: float


class CreateGroup(BaseModel):
    title: str
    occupation: str
    curator: str
    since: int
    bonus: bool


class UpdateGroup(BaseModel):
    curator: str
    bonus: bool