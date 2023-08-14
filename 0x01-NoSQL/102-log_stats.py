#!/usr/bin/env python3
"""
Log stats - new version
"""

from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx

    total_logs = logs_collection.count_documents({})

    print("{} logs".format(total_logs))

    # Count methods
    methods = logs_collection.aggregate([
        {"$group": {"_id": "$method", "count": {"$sum": 1}}}
    ])
    print("Methods:")
    for method in methods:
        print("\tmethod {}: {}".format(method['_id'], method['count']))

    # Count status checks
    status_checks = logs_collection.count_documents(
        {"method": "GET", "path": "/status"})
    print("{} status check".format(status_checks))

    # Count IPs and get the top 10
    ip_counts = logs_collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])
    print("IPs:")
    for ip_count in ip_counts:
        print("\t{}: {}".format(ip_count['_id'], ip_count['count']))
