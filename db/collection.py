"""
A simple mongodb helper
"""
from pymongo import MongoClient

from config import Config


def get_repo_collection():
    """Getting 'repositories' collection"""
    client = MongoClient(Config.MONGO_HOST, Config.MONGO_PORT)
    db = client[Config.MONGO_DBNAME]
    repositories = db['repositories']
    return repositories
