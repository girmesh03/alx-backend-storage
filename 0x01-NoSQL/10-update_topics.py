#!/usr/bin/env python3
"""A Python function that changes all topics of a
school document based on the name:"""


def update_topics(mongo_collection, name, topics):
    """A Python function that changes all topics of a
    school document based on the name:"""
    if mongo_collection is None:
        return []
    return mongo_collection.update_many(
        {"name": name}, {"$set": {"topics": topics}})
