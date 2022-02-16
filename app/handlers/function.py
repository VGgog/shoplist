import random

from database import shoplist_collection, users_collection
from database import crud


def generate_group_id():
    """
    Return group id whith not in MongoDB 
    """
    group_id = generate_code()
    while crud.find_group(shoplist_collection, group_id):
        group_id = generate_code()

    return group_id


def generate_code():
    """
    Generate 6 digit code
    """
    return random.randrange(100000, 999999)


def get_shoplist(group_id):
    """
    get shoplist
    """
    group_data = crud.find_group(shoplist_collection, {"_id": group_id})
    return group_data["shoplist"]


def get_user_message(products):
    """
    get user message all products in shoplist
    """
    i = 1
    user_message = ''
    for product in products:
        user_message += "{}) {}\n".format(i, product)
        i += 1

    return user_message


def get_data_for_user_collection(group_id, user_id):
    """
    get data for add in users collection
    """
    return {
        "group_id": group_id,
        "user_id": user_id
    }
