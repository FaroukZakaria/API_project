import jwt
from bson import ObjectId
from flask_jwt_extended import decode_token
from project.db import *
from project.models.user_model import User

def verify_token(token):
    try:
        return decode_token(token)
    except jwt.ExpiredSignatureError:
        #print("Token has expired.")
        return None
    except jwt.InvalidTokenError:
        #print("Invalid token.")
        return None
    except Exception as e:
        #print(f"An unexpected error occurred: {e}")
        return None

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

def refresh_token(token):
    try:
        return decode_token(token)
    except jwt.ExpiredSignatureError:
        #print("Token has expired.")
        return None
    except jwt.InvalidTokenError:
        #print("Invalid token.")
        return None
    except Exception as e:
        #print(f"An unexpected error occurred: {e}")
        return None