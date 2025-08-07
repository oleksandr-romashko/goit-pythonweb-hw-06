"""
Validation utility functions for model various field types.

These validators are intended for use with SQLAlchemy's @validates decorators
to enforce domain-level validation rules across models.
"""

import datetime


def validate_text_field(
    key: str, value: str, min_len: int = 0, max_len: int = 0
) -> str:
    """Validate that a text field is non-empty and within length limits."""
    if max_len < min_len:
        raise ValueError(f"Invalid configuration for '{key}': max_len < min_len")

    if value is None:
        raise ValueError(f"Field '{key}' cannot be None")

    # Normalize
    value = value.strip()

    if not value:
        raise ValueError(f"Field '{key}' cannot be empty")
    if len(value) < min_len:
        raise ValueError(f"Field '{key}' must be at least {min_len} characters long")
    if len(value) > max_len:
        raise ValueError(f"Field '{key}' must be less than {max_len} characters long")

    return value


def validate_date(key: str, value: datetime.date) -> datetime.date:
    """Validate that a value is a datetime.date instance."""
    if not isinstance(value, datetime.date):
        raise ValueError(f"Field '{key}' must be a valid date object")

    return value


def validate_positive_number(key: str, value: int | str) -> int:
    """Validate that grade is a positive integer (accepts numeric strings)."""
    if value is None:
        raise ValueError(f"Field '{key}' cannot be None")

    # Convert string to int if possible
    if isinstance(value, str):
        if not value.isdigit():
            raise ValueError(f"Field '{key}' must be a positive integer, got '{value}'")
        value = int(value)

    if not isinstance(value, int):
        raise ValueError(
            f"Field '{key}' must be an integer, got {type(value).__name__}"
        )

    if value <= 0:
        raise ValueError(f"Field '{key}' must be a positive integer, got {value}")

    return value
