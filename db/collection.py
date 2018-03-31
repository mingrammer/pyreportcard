"""
A simple mongodb helper
"""
from config import Config
from pymongo import MongoClient


def get_repo_collection():
    """Getting 'repositories' collection"""
    client = MongoClient(Config.MONGO_HOST, Config.MONGO_PORT)
    db = client[Config.MONGO_DBNAME]
    repositories = db['repositories']
    return repositories
