"""
ORM model for Group entity.
"""

import datetime

from sqlalchemy import String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .associations import group_subject_association_table
from .base_model import BaseModel
from .grade import Grade
from .student import Student
from .subject import Subject


class Group(BaseModel):
    """
    Represents a students group.

    A group can have many students and many subjects.
    Used to track academic groups, start dates, and related performance.
    """

    __tablename__ = "groups"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    start_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)

    students: Mapped[list["Student"]] = relationship(back_populates="group")
    subjects: Mapped[list["Subject"]] = relationship(
        secondary=group_subject_association_table, back_populates="groups"
    )
    grades: Mapped[list["Grade"]] = relationship(back_populates="group")
