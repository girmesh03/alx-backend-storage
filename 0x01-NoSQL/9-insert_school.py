#!/usr/bin/env python3
"""A Python function that changes all topics of a
school document based on the name"""


def insert_school(mongo_collection, **kwargs):
    """A Python function that changes all topics of a
    school document based on the name:"""
    if mongo_collection is None:
        return []
    return mongo_collection.insert_one(kwargs).inserted_id
