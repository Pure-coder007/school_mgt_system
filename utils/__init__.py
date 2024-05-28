import uuid
import re


def hexid():
    return uuid.uuid4().hex


def is_valid_email(email):
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return True
    return False


# This function determines the grade based on the score.
def get_grade(score):
    # The if statement checks the score and assigns the grade
    # if the score is greater than or equal to 80, the grade is A
    if score >= 80:
        return 'A'
    # if the score is greater than or equal to 65, the grade is B
    elif score >= 65:
        return 'B'
    # if the score is greater than or equal to 55, the grade is C
    elif score >= 55:
        return 'C'
    # if the score is greater than or equal to 40, the grade is D
    elif score >= 40:
        return 'D'
    # if the score is less than 40, the grade is F
    else:
        return 'F'
