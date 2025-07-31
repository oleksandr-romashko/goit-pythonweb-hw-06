"""
ORM model for Teacher entity, inheriting person-related fields.
"""

from .person import Person


class Teacher(Person):
    """
    Represents a teacher with common person attributes.
    """

    __tablename__ = "teachers"
