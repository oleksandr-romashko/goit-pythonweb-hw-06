"""
ORM model for Student entity.
"""

from typing import TYPE_CHECKING
import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import BaseModel

# Used for type hints only; avoids circular imports at runtime
if TYPE_CHECKING:
    from .grade import Grade
    from .group import Group
    from .personal_data import PersonalData


class Student(BaseModel):
    """
    Represents a student with a reference to their assigned group.
    """

    __tablename__ = "students"

    group_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("groups.id", ondelete="SET NULL"), nullable=True
    )

    personal_data_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("personal_data.id"), nullable=False, unique=True
    )

    group: Mapped["Group"] = relationship(back_populates="students")
    grades: Mapped[list["Grade"]] = relationship(back_populates="student")
    personal_data: Mapped["PersonalData"] = relationship()
