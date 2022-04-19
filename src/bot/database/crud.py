"""
Module for create, read, update, delete document in MongoDB database.
"""


def create_document(collection, data):
    """
    Create new document in collection.
    """
    return collection.insert_one(data).inserted_id


def find_document(collection, data):
    """
    Find document in collection.
    """
    return collection.find_one(data)


def update_document(collection, element, new_value):
    """
    Function for update document in collection.
    """
    return collection.update_one(element, {'$set': new_value})


def delete_document(collection, data):
    """
    Function for delete document in collection.
    """
    return collection.delete_one(data)
