import random 
from database.crud import find_group


def generate_group_id():
    """
    Return group id whith not in MongoDB 
    """
    group_id = generate_code()
    while find_group(group_id):
        group_id = generate_code()

    return group_id


def generate_code():
    """
    Generate 6 digit code
    """
    return random.randrange(100000, 999999)
