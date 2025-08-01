"""
ORM model for Teacher entity.
"""

import uuid


from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import BaseModel
from .personal_data import PersonalData
from .subject import Subject


class Teacher(BaseModel):
    """
    Represents a teacher with a reference to their assigned subject.
    """

    __tablename__ = "teachers"

    subjects: Mapped[list["Subject"]] = relationship(back_populates="teacher")
    personal_data_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("personal_data.id"), nullable=False, unique=True
    )

    personal_data: Mapped["PersonalData"] = relationship()
