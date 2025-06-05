import re


def validate_email(email: str) -> bool:
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None


def validate_phone(phone: str) -> bool:
    # Accepts phone numbers with optional '+' and 10-15 digits
    return re.match(r"^\+?\d{10,15}$", phone) is not None
