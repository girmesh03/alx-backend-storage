#!/usr/bin/env python3
"""
Log stats - new version
"""

from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx

    total_logs = logs_collection.count_documents({})

    print(f"{total_logs} logs")

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {method: logs_collection.count_documents(
        {"method": method}) for method in methods}

    print("Methods:")
    for method, count in method_counts.items():
        print(f"    method {method}: {count}")

    status_checks = logs_collection.count_documents(
        {"method": "GET", "path": "/status"})

    print(f"{status_checks} status check")

    pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]

    top_ips = logs_collection.aggregate(pipeline)

    print("IPs:")
    for ip in top_ips:
        print(f"    {ip['_id']}: {ip['count']}")
