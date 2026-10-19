
from passlib.context import CryptContext
import re

# Password hashing configuration
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)



def hash_password(password):
    if len(password.encode("utf-8")) > 72:
        raise ValueError("Password must not exceed 72 bytes.")

    return pwd_context.hash(password)


# Verify a password during login
def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


# Validate username
def validate_username(username):
    if len(username) < 3:
        return False, "Username must be at least 3 characters."

    if not re.match(r"^[a-zA-Z0-9_]+$", username):
        return False, "Only letters, numbers, and underscores allowed."

    return True, ""


# Validate email
def validate_email(email):
    if not re.match(r"^[\w.-]+@[\w.-]+\.\w+$", email):
        return False, "Invalid email format."

    return True, ""



def validate_password(password):
    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    if len(password.encode("utf-8")) > 72:
        return False, "Password must not exceed 72 bytes."

    if not any(c.isdigit() for c in password):
        return False, "Password must contain a digit."

    if not any(c.isalpha() for c in password):
        return False, "Password must contain a letter."

    return True, ""