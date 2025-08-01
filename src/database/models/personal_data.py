"""
ORM abstract model for general person-related fields.
"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base_model import BaseModel


class PersonalData(BaseModel):
    """
    Table to store personal information that can be linked to multiple entity types
    (e.g. Student, Teacher). Useful for GDPR compliance (anonymization, soft delete, etc).
    """

    __tablename__ = "personal_data"

    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    # birth_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    # phone_number: Mapped[str | None] = mapped_column(String(20), nullable=True)
    # email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    # photo_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    # bio: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    # TODO: Add address -> foreign key to a separate table (database normalization)
    # TODO: Add gender (if necessary) -> enum male/female/other to allow filtering/statistics
