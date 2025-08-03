"""
Package for all ORM models.

Includes SQLAlchemy models and association tables.
Exposes Base for metadata management and migrations.
"""

from .base import Base

from .grade import Grade
from .group import Group
from .personal_data import PersonalData
from .student import Student
from .subject import Subject
from .teacher import Teacher

from .associations import group_subject_association_table

__all__ = [
    "Base",
    "Grade",
    "Group",
    "PersonalData",
    "Student",
    "Subject",
    "Teacher",
    "group_subject_association_table",
]
