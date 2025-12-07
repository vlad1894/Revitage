from pymongo import MongoClient
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password


client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB_NAME]

users_collection = db["users"]
products_collection = db["products"]  # we'll use this later for catalog, if you want


def create_user(email: str, password: str, full_name: str | None = None):
    existing = users_collection.find_one({"email": email})
    if existing:
        raise ValueError("Email already registered")

    user_doc = {
        "email": email,
        "password_hash": make_password(password),
        "full_name": full_name,
        "is_active": True,
    }

    result = users_collection.insert_one(user_doc)
    user_doc["_id"] = result.inserted_id
    return user_doc


def authenticate_user(email: str, password: str):
    user = users_collection.find_one({"email": email})
    if not user:
        return None

    if not check_password(password, user["password_hash"]):
        return None

    return user