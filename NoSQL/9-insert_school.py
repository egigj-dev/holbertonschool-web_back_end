#!usr/bin/env python3
"""Script that inserts a new document based on kwargs"""

def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document in a collection based on kwargs
    """
    result = mongo_collection.insertOne(kwargs)
    return result.inserted_id
