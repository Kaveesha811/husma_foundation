import hashlib
import secrets
from database.operations import get_donor_by_username, get_donor_by_email


def hash_password(password):
    """Hash password using SHA-256 (simplified for compatibility)"""
    salt = secrets.token_hex(16)
    return f"{salt}${hashlib.sha256((salt + password).encode()).hexdigest()}"


def check_password(hashed_password, user_password):
    """Check password against hash"""
    try:
        salt, stored_hash = hashed_password.split('$')
        computed_hash = hashlib.sha256((salt + user_password).encode()).hexdigest()
        return computed_hash == stored_hash
    except Exception:
        return False


def authenticate_user(username, password):
    """Authenticate user with username/email and password"""
    # Try username first
    donor = get_donor_by_username(username)
    if not donor:
        # Try email
        donor = get_donor_by_email(username)

    if donor and check_password(donor['password'], password):
        return donor
    return None


def validate_password_strength(password):
    """Validate password meets strength requirements"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)

    if not all([has_upper, has_lower, has_digit, has_special]):
        return False, "Password must contain uppercase, lowercase, digit, and special character"

    return True, "Password is strong"