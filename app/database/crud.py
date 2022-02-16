def create_a_group_doc(collection, data):
    """
    Creating new group in MongoDB.
    """
    return collection.insert_one(data).inserted_id


def find_group(collection, data):
    """
    Find group in MongoDB
    """
    return collection.find_one(data)


def update_document(collection, element, new_value):
    """
    """
    return collection.update_one(element, {'$set': new_value})

