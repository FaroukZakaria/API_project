import jwt
from flask_jwt_extended import decode_token
from flask import current_app

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

def is_refresh_token_revoked(refresh_token):
    return current_app.redis.exists(refresh_token)