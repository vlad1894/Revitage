# shop/mongo_client.py
from pymongo import MongoClient
from django.conf import settings

_client = MongoClient(settings.MONGO_URI)
_db = _client[settings.MONGO_DB_NAME]

def get_users_collection():
    return _db["users"]

def get_products_collection():
    return _db["products"]

def get_carts_collection():
    return _db["carts"]