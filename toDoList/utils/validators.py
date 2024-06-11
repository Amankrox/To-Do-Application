import re

def validate_name(name):
    return name.isalpha()

def validate_phone(phone):
    return re.match(r'^\d{10}$', phone)

def validate_email(email):
    return re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email)

def validate_password(password):
    if len(password) < 7:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[^a-zA-Z0-9]', password):
        return False
    return True
