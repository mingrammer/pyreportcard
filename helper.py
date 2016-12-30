"""
A collection of helper functions
"""
from config import MONGO_DB
from pymongo import MongoClient


def get_repo_collection():
    """Getting collection for repository"""
    client = MongoClient(MONGO_DB['HOST'], MONGO_DB['PORT'])
    db = client[MONGO_DB['DB_NAME']]
    repositories = db[MONGO_DB['REPOSITORIES_COLLECTION']]
    return repositories
