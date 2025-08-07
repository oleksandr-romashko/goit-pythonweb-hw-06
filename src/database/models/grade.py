"""
ORM model for Grade entity.
"""

from typing import TYPE_CHECKING
import uuid

from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from utils.constants import MIN_TASK_LEN, MAX_TASK_LEN
from utils.validators import validate_text_field, validate_positive_number

from .base_model import BaseModel

# Used for type hints only; avoids circular imports at runtime
if TYPE_CHECKING:
    from .group import Group
    from .student import Student
    from .subject import Subject


class Grade(BaseModel):
    """
    Represents a grade for a student, tied to a group, subject, and specific task.
    Allows multiple grades per subject if tied to different tasks.
    """

    __tablename__ = "grades"
    __table_args__ = (
        UniqueConstraint(
            "student_id", "group_id", "subject_id", "task_number", name="uq_grade_task"
        ),
    )

    task_number: Mapped[int] = mapped_column(Integer, nullable=False)
    grade: Mapped[int] = mapped_column(Integer, nullable=False)

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
    )
    group_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("groups.id", ondelete="CASCADE"), nullable=False
    )
    subject_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("subjects.id", ondelete="CASCADE"),
        nullable=False,
    )

    # TODO: Make task a separate table or enum (repetitive or standardized
    # (e.g. Quiz, Exam, Project))
    # TODO: Add grade a separate table
    # (for grade type, e.g. Numeric (0-100), Letter (A-F), Pass/Fail, Max score, Weight)

    student: Mapped["Student"] = relationship(back_populates="grades")
    group: Mapped["Group"] = relationship(back_populates="grades")
    subject: Mapped["Subject"] = relationship(back_populates="grades")

    def __repr__(self) -> str:
        subject_name = self.subject.title if self.subject else "Unknown Subject"
        group_name = self.group.name if self.group else "Unknown Group"

        return (
            f"<Grade(task='{self.task_number}', grade={self.grade}, "
            f"student='{self.student_id}', subject='{subject_name}', group='{group_name}')>"
        )

    @validates("task_number")
    def validate_task_number(self, key, value) -> int:
        """Validate task number"""
        return validate_positive_number(key, value)

    @validates("grade")
    def validate_grade(self, key, value) -> int:
        """Validate grade"""
        return validate_positive_number(key, value)
