from jose import jwt
from datetime import datetime, timedelta, timezone
from config import get_auth_data


"""
JWT token creation utilities.
Handles generation of access tokens for user authentication.
"""

def create_access_token(data: dict) -> str:
    """
    Create JWT access token with expiration.
    
    :param data: Payload data to encode in token
    :return: Encoded JWT token string
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)  # Token expires in 30 minutes
    to_encode.update({"exp": expire})

    auth_data = get_auth_data()
    encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return encode_jwt
