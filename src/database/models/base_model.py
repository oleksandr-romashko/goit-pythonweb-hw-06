"""Abstract base model combining all common mixins."""

from .base import Base
from .mixins import UUIDMixin, TimestampMixin, SoftDeleteMixin


class BaseModel(UUIDMixin, TimestampMixin, SoftDeleteMixin, Base):
    """Abstract base class for all models in the system."""

    __abstract__ = True
