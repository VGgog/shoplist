import random

from .database import crud, shoplist_collection, users_collection


def generate_group_id():
    """
    Return group id which not in MongoDB.
    """
    group_id = generate_code()
    while crud.find_document(shoplist_collection, group_id):
        group_id = generate_code()

    return group_id


def generate_code():
    """
    Generate 6 digit code.
    """
    return random.randrange(100000, 999999)


def get_shoplist(user_id):
    """
    Get shoplist from shoplist_collection.
    """
    group_data = crud.find_document(shoplist_collection, {"_id": get_group_id(user_id)})
    return group_data["shoplist"]


def message_which_shopping_list(products):
    """
    Get string numbered list with all products in shoplist for the user's message.
    """
    i = 1
    user_message = ''
    for product in products:
        user_message += "{}) {}\n".format(i, product)
        i += 1

    return user_message


def get_data_for_users_collection(group_id, user_id):
    """
    Get data for add in users_collection.
    """
    return {
        "group_id": group_id,
        "user_id": user_id
    }


def get_group_id(user_id):
    """
    Get group id in which consist user.
    """
    user_info = crud.find_document(users_collection, {"user_id": user_id})
    return user_info["group_id"]
