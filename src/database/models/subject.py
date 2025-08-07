"""
ORM model for Subject entity.
"""

from typing import TYPE_CHECKING
import uuid

from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from utils.constants import MIN_SUBJECT_TITLE_LEN, MAX_SUBJECT_TITLE_LEN
from utils.validators import validate_text_field

from .associations import group_subject_association_table
from .base_model import BaseModel

# Used for type hints only; avoids circular imports at runtime
if TYPE_CHECKING:
    from .grade import Grade
    from .group import Group
    from .teacher import Teacher


class Subject(BaseModel):
    """
    Represents a subject to study.

    Each subject is taught by a teacher, can be associated with multiple groups,
    and can have many grades from students.
    """

    __tablename__ = "subjects"

    # TODO: Evaluate unique=True constraint for the subject title
    title: Mapped[str] = mapped_column(String(MAX_SUBJECT_TITLE_LEN), nullable=False)
    teacher_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("teachers.id"),
        nullable=False,
    )

    teacher: Mapped["Teacher"] = relationship(back_populates="subjects")
    groups: Mapped[list["Group"]] = relationship(
        secondary=group_subject_association_table, back_populates="subjects"
    )
    grades: Mapped[list["Grade"]] = relationship(back_populates="subject")

    def __repr__(self) -> str:
        return f"<Subject(id={self.id!r}, title={self.title!r}, teacher_id={self.teacher_id!r})>"

    @validates("title")
    def validate_title(self, key, value) -> str:
        """Validate title"""
        return validate_text_field(
            key, value, min_len=MIN_SUBJECT_TITLE_LEN, max_len=MAX_SUBJECT_TITLE_LEN
        )
