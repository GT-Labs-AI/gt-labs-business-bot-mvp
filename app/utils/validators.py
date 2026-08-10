import re


def validate_phone(phone: str) -> bool:
    """Validates mobile phone number format (supports international formats)."""
    cleaned = re.sub(r"[\s\-\(\)]", "", phone)
    pattern = r"^\+?[1-9]\d{8,14}$"
    return bool(re.match(pattern, cleaned))