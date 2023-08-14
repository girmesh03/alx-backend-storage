#!/usr/bin/env python3
"""A Python script that provides some stats
about Nginx logs stored in MongoDB:"""

from pymongo import MongoClient


def nginx_stats():
    """ Provides some stats about Nginx logs stored in MongoDB """
    client = MongoClient()
    collection = client.logs.nginx

    num_of_docs = collection.count_documents({})
    print("{} logs".format(num_of_docs))

    # methods list
    methods_list = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")

    for method in methods_list:
        method_count = collection.count_documents({"method": method})
        print("\tmethod {}: {}".format(method, method_count))

    # status check
    status = collection.count_documents({"method": "GET", "path": "/status"})
    print("{} status check".format(status))


if __name__ == "__main__":
    nginx_stats()
