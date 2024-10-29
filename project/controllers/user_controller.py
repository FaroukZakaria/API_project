from bson import ObjectId
from project.db import *
from project.models.user_model import User

# Function to insert a user
def create_user(user_data: User):
    user_dict = user_data.dict()
    result = users_collection.insert_one(user_dict)
    return result.inserted_id

# Function to get a user by email
def get_user_by_email(email):
    user = users_collection.find_one({"email": email})
    if not user:
        return None
    return user

# Function to get a user by ID
def get_user_by_id(user_id):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        return None
    return user

# Function to delete a user
def delete_user(user_id):
    result = users_collection.delete_one({"_id": ObjectId(user_id)})
    return result