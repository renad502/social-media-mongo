from pydantic import EmailStr
import re

def validate_email(email: str) -> bool:
    # Basic validation using pydantic's EmailStr
    try:
        _ = EmailStr.validate(email)
        return True
    except Exception:
        return False

def validate_username(username: str) -> bool:
    # Username must be alphanumeric, 3-30 characters
    pattern = r'^[a-zA-Z0-9_]{3,30}$'
    return bool(re.match(pattern, username))

def validate_password(password: str) -> bool:
    # Password must be at least 8 chars, with a number and a letter
    if len(password) < 8:
        return False
    if not re.search(r'[A-Za-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    return True
