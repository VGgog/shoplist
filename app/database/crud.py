from database import collection


def create_a_group_doc(data):
    """
    Creating new group in MongoDB.
    """
    return collection.insert_one(data).inserted_id


def find_group(data):
    """
    Find group in MongoDB
    """
    return collection.find_one(data)


def update_document(element, new_value):
    """
    """
    return collection.update_one(element, {'$set': new_value})

