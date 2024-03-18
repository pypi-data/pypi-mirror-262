import os

from pymongo import MongoClient

DEFAULT_MONGO_URL = "mongodb:root@example//localhost:27017/"


def get_mongo_url():
    return os.getenv('MONGO_URL', DEFAULT_MONGO_URL)


def get_mongo_client():
    return MongoClient(get_mongo_url())
