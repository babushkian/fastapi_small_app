from pydantic import BaseModel, ConfigDict, Field
from typing import List

class CourseBase(BaseModel):
    title: str

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class StudentBase(BaseModel):
    name: str

class StudentCreate(StudentBase):
    pass


class StudentNew(StudentBase):
    id: int



class Student(StudentNew):
    courses: List[Course] = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)