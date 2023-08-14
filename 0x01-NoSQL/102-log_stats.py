#!/usr/bin/env python3
""" Log stats - new version """
from pymongo import MongoClient


def nginx_stats_check():
    """ provides some stats about Nginx logs stored in MongoDB:"""
    client = MongoClient()
    collection = client.logs.nginx

    total_logs = collection.count_documents({})

    print(f"{total_logs} logs")

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {method: collection.count_documents(
        {"method": method}) for method in methods}

    print("Methods:")
    for method, count in method_counts.items():
        print(f"    method {method}: {count}")

    status_checks = collection.count_documents(
        {"method": "GET", "path": "/status"})

    print(f"{status_checks} status check")

    pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]

    top_ips = collection.aggregate(pipeline)

    print("IPs:")
    for ip in top_ips:
        print(f"{ip['_id']}: {ip['count']}")


if __name__ == "__main__":
    nginx_stats_check()
