# fast_api_post_manager/utils/validation.py

import re
import uuid


def validate_id(value):
    """
    Validate that the value is a valid UUID.
    """
    try:
        return uuid.UUID(str(value))
    except ValueError:
        raise ValueError("Invalid UUID format")


def validate_name(value):
    """
    Validate that the name is a valid string.
    """
    if not value or not value.strip():
        raise ValueError("Name cannot be empty")
    if len(value) < 2:
        raise ValueError("Name must be at least 2 characters long")
    if len(value) > 50:
        raise ValueError("Name must be at most 50 characters long")
    return value


def validate_empty(value):
    """
    Validate that the value is not empty.
    """
    if not value or not str(value).strip():
        raise ValueError("Value cannot be empty")
    return value


def validate_password(value):
    """
    Validate password complexity.
    """
    if len(value) < 8:
        raise ValueError("Password must be at least 8 characters long")
    if not re.search(r'[A-Z]', value):
        raise ValueError("Password must contain at least one uppercase letter")
    if not re.search(r'[0-9]', value):
        raise ValueError("Password must contain at least one number")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        raise ValueError("Password must contain at least one special character")
    return value


def validate_email(email: str) -> str:
    """
    Validate email format.
    """
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        raise ValueError("Invalid email format")
    return email


def validate_text(text):
    if len(text.encode('utf-8')) > 1048576:  # 1MB in bytes
        raise ValueError('Text size exceeds 1MB limit')
    return text


def validate_status(status):
    if status not in ['draft', 'published']:
        raise ValueError('Status must be either draft or published')
    return status
