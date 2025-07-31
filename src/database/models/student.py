"""
ORM model for Student entity, inheriting personal fields from Person.
"""

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .person import Person


class Student(Person):
    """
    Represents a student with a reference to their assigned group.
    """

    __tablename__ = "students"

    group_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("groups.id"), nullable=True
    )
