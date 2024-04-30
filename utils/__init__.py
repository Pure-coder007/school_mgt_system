import uuid
import re


def hexid():
    return uuid.uuid4().hex


def is_valid_email(email):
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return True
    return False
