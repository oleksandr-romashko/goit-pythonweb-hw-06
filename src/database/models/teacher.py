"""
ORM model for Teacher entity.
"""

from typing import TYPE_CHECKING
import uuid


from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import BaseModel

# Used for type hints only; avoids circular imports at runtime
if TYPE_CHECKING:
    from .personal_data import PersonalData
    from .subject import Subject


class Teacher(BaseModel):
    """
    Represents a teacher with a reference to their assigned subject.
    """

    __tablename__ = "teachers"

    # TODO: ADD hire_date

    subjects: Mapped[list["Subject"]] = relationship(back_populates="teacher")
    personal_data_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("personal_data.id"), nullable=False, unique=True
    )

    personal_data: Mapped["PersonalData"] = relationship()

    def __repr__(self) -> str:
        return (
            f"Teacher("
            f"id={self.id!r}, "
            f"personal_data_id={self.personal_data_id!r})"
        )
