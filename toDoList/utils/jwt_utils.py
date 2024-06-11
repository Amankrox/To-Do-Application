# project/utils/jwt_utils.py
import jwt
from datetime import datetime,timedelta
import logging

SECRET_KEY = 'PwNvxcbnqDJqsto9J-wO8WqgtFI9MKNB9jNcc8Rj9nU'

def encode_jwt(payload,exp=24*60):
    payload['exp'] = datetime.utcnow() + timedelta(minutes=exp)
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def decode_jwt(token):
    # Remove the Bearer from the token if it exists
    if token is None:
        logging.error("Token is None")
        return None
    
    # Remove the Bearer from the token if it exists
    try:
        token = token.replace("Bearer ", "")
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        return decoded_token
    except jwt.ExpiredSignatureError:
        logging.error("Token has expired")
        return None
    except jwt.InvalidTokenError:
        logging.error("Invalid token")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return None