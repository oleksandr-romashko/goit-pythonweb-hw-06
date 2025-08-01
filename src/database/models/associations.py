"""
SQLAlchemy association tables for many-to-many relationships.
"""

from sqlalchemy import Table, Column, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import UUID

from .base import Base

# Association table for many-to-many relation between groups and subjects
group_subject_association_table = Table(
    "group_subject_association",
    Base.metadata,
    Column(
        "group_id",
        UUID(as_uuid=True),
        ForeignKey("groups.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column(
        "subject_id",
        UUID(as_uuid=True),
        ForeignKey("subjects.id", ondelete="CASCADE"),
        nullable=False,
    ),
    PrimaryKeyConstraint("group_id", "subject_id", name="pk_group_subject_association"),
)
