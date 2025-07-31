"""
ORM abstract model for general person-related fields to be reused by concrete entities like Student or Teacher.
"""

import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base_model import BaseModel


class Person(BaseModel):
    """
    Abstract base class for a person entity. Contains common personal attributes
    such as name, birth date, contact information, and bio.
    """

    __abstract__ = True

    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    birth_date: Mapped[datetime.date]
    phone_number: Mapped[str | None] = mapped_column(String(20), nullable=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    photo_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    bio: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    # TODO: Add address -> foreign key to a separate table (normalization)
    # TODO: Add gender -> enum male/female/other to allow filtering/statistics
