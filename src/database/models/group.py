"""
ORM model for Group entity.
"""

import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from utils.constants import MIN_NAME_LEN, MAX_NAME_LEN
from utils.validators import validate_text_field, validate_date

from .associations import group_subject_association_table
from .base_model import BaseModel

# Used for type hints only; avoids circular imports at runtime
if TYPE_CHECKING:
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

    name: Mapped[str] = mapped_column(String(MAX_NAME_LEN), nullable=False)
    start_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)

    students: Mapped[list["Student"]] = relationship(back_populates="group")
    subjects: Mapped[list["Subject"]] = relationship(
        secondary=group_subject_association_table, back_populates="groups"
    )
    grades: Mapped[list["Grade"]] = relationship(back_populates="group")

    def __repr__(self) -> str:
        return f"<Group(id={self.id!r}, name={self.name!r}, start_date={self.start_date!r})>"

    @validates("name")
    def validate_name(self, key, value) -> str:
        """Validate name"""
        return validate_text_field(
            key, value, min_len=MIN_NAME_LEN, max_len=MAX_NAME_LEN
        )

    @validates("start_date")
    def validate_start_date(self, key, value) -> datetime.date:
        """Validate start_date is a date instance."""
        return validate_date(key, value)
