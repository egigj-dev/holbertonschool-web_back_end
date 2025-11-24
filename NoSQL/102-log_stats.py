#!/usr/bin/env python3
"""
Script that provides stats about Nginx logs stored in MongoDB
Includes top 10 most present IPs
"""
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx
    
    # Total number of logs
    total_logs = nginx_collection.count_documents({})
    print("{} logs".format(total_logs))
    
    # Methods stats
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = nginx_collection.count_documents({"method": method})
        print("\tmethod {}: {}".format(method, count))
    
    # Status check count
    status_check = nginx_collection.count_documents({
        "method": "GET",
        "path": "/status"
    })
    print("{} status check".format(status_check))
    
    # Top 10 IPs
    print("IPs:")
    pipeline = [
        {
            "$group": {
                "_id": "$ip",
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {"count": -1}
        },
        {
            "$limit": 10
        }
    ]
    
    top_ips = nginx_collection.aggregate(pipeline)
    for ip_doc in top_ips:
        print("\t{}: {}".format(ip_doc.get('_id'), ip_doc.get('count')))
