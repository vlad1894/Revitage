from pymongo import MongoClient, errors
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password


client = MongoClient(
    settings.MONGO_URI,
    serverSelectionTimeoutMS=5000,
    connectTimeoutMS=5000,
    socketTimeoutMS=5000,
)
db = client[settings.MONGO_DB_NAME]

users_collection = db["users"]
products_collection = db["products"]  # we'll use this later for catalog, if you want


def create_user(username: str, email: str, password: str, full_name: str | None = None):
    try:
        existing_username = users_collection.find_one({"username": username})
        if existing_username:
            raise ValueError("Username already taken")
        existing_email = users_collection.find_one({"email": email})
        if existing_email:
            raise ValueError("Email already registered")

        user_doc = {
            "username": username,
            "email": email,
            "password_hash": make_password(password),
            "full_name": full_name,
            "is_active": True,
        }

        result = users_collection.insert_one(user_doc)
        user_doc["_id"] = result.inserted_id
        return user_doc
    except errors.PyMongoError as exc:
        raise ValueError("Database unavailable. Please try again.") from exc


def authenticate_user(username_or_email: str, password: str):
    try:
        user = users_collection.find_one({"username": username_or_email})
        if not user:
            user = users_collection.find_one({"email": username_or_email})
        if not user:
            return None

        if not check_password(password, user["password_hash"]):
            return None

        return user
    except errors.PyMongoError:
        return None
