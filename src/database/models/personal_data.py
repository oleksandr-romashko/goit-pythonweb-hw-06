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

    # TODO: ADD birth_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    # TODO: ADD phone_number: Mapped[str | None] = mapped_column(String(20), nullable=True)
    # TODO: ADD email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    # TODO: ADD photo_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    # TODO: ADD bio: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    # TODO: Add address -> foreign key to a separate table (database normalization)
    #  address_id: Mapped[uuid.UUID | None] = mapped_column(
    #      UUID(as_uuid=True), ForeignKey("addresses.id"), nullable=True
    #  )
    # TODO: Add gender (if necessary) -> enum male/female/other to allow filtering/statistics
    # class Gender(enum.Enum):
    #     male = "male"
    #     female = "female"
    #     other = "other"
    # gender: Mapped[Gender | None] = mapped_column(Enum(Gender), nullable=True)
