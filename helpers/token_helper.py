from fastapi import Request, HTTPException, status
from fastapi import Response

from jose import jwt, JWTError
from datetime import datetime, timezone
from config import get_auth_data


"""
JWT token validation and extraction utilities.
Handles token verification and user identification.
"""


def get_token(request: Request, response: Response) -> str:
    """
    Extract JWT token from request cookies or Authorization header.
    
    :param request: FastAPI request object
    :param response: FastAPI response object
    :return: Token string
    :raises HTTPException: 401 if token not found
    """
    token = request.cookies.get('user_access_token')
    if not token:
        token = request.headers.get('Authorization')
        if token:
            token = token.split(" ")[1] # Remove "Bearer " prefix
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token not found')

    return token


def verify_token(token: str) -> str:
    """
    Verify JWT token validity and extract user ID.
    
    :param token: JWT token to verify
    :return: User ID from token payload
    :raises HTTPException: 401 if token invalid or expired
    """
    try:
        auth_data = get_auth_data()
        payload = jwt.decode(token, auth_data['secret_key'], auth_data['algorithm'])

    except JWTError:
        print("Token is not valid")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is not valid')

    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        print("Token has expired")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token has expired')

    user_id = payload.get('sub')
    if not user_id:
        print("User's id not found")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User's id not found")

    return user_id
