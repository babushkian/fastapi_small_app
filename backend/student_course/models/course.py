from sqlalchemy import Integer, String, Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base
# from models import Student



student_course = Table(
    "student_course",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
    Column("course_id", Integer, ForeignKey("courses.id"), primary_key=True),
)


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)

    students: Mapped[list["Student"]] = relationship(
        "Student",
        secondary=student_course,
        back_populates="courses",
        lazy="selectin",
    )

