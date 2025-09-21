from sqlalchemy import Table, Column, String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import Base






class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)

    courses: Mapped[list["Course"]] = relationship(
        "Course",
        secondary="student_course",
        back_populates="students",
        lazy="selectin",
    )

