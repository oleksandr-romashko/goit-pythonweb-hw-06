"""
ORM model for Grade entity.
"""

import uuid

from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import BaseModel
from .student import Student
from .group import Group
from .subject import Subject


class Grade(BaseModel):
    """
    Represents a grade for a student, tied to a group, subject, and specific task.
    Allows multiple grades per subject if tied to different tasks.
    """

    __tablename__ = "grades"
    __table_args__ = (
        UniqueConstraint(
            "student_id", "group_id", "subject_id", "task", name="uq_grade_task"
        ),
    )

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
    task: Mapped[str] = mapped_column(String(100), nullable=False)
    # TODO: Add grade a separate table
    # (for grade type, e.g. Numeric (0-100), Letter (A-F), Pass/Fail, Max score, Weight)
    grade: Mapped[int] = mapped_column(Integer, nullable=False)

    student: Mapped["Student"] = relationship(back_populates="grades")
    group: Mapped["Group"] = relationship(back_populates="grades")
    subject: Mapped["Subject"] = relationship(back_populates="grades")
