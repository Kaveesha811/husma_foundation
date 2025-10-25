import re


def validate_nic(nic):
    """Validate NIC format for Sri Lanka"""
    nic = nic.strip().upper()

    if len(nic) == 10:  # Old format
        if not nic[:-1].isdigit():
            return False
        if nic[-1] not in ['V', 'X']:
            return False
        return True
    elif len(nic) == 12:  # New format
        return nic.isdigit()

    return False


def validate_phone(phone):
    """Validate Sri Lankan phone number"""
    phone = phone.strip()
    phone = phone.replace(' ', '').replace('-', '')
    return len(phone) == 10 and phone.isdigit()


def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password):
    """Validate password format"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters"

    checks = [
        (r'[A-Z]', "uppercase letter"),
        (r'[a-z]', "lowercase letter"),
        (r'\d', "digit"),
        (r'[!@#$%^&*(),.?":{}|<>]', "special character")
    ]

    for pattern, requirement in checks:
        if not re.search(pattern, password):
            return False, f"Password must contain at least one {requirement}"

    return True, "Password is valid"