from starlette.responses import Response

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from DAO.user_dao import UserDAO
from database import schema
from helpers import password_helper
from helpers.jwt_helper import create_access_token


"""
User authentication helper functions.
Handles login process and token generation.
"""


async def take_access_token_for_user(db: AsyncSession, 
                                     response: Response, 
                                     request: schema.UserSignIn):
    """
    Authenticate user and generate access token.
    
    :param db: Database session
    :param response: Response object to set cookies
    :param request: User login credentials
    :return: User info with access token or error
    """

    # Get user by email
    user = await UserDAO.get_user_email(db=db, user_email=str(request.email))

    # Check if user exists
    if not user:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {
            'message': "Invalid email and/or password",
            'status_code': 403,
            'error': "FORBIDDEN"
        }

    # Verify password
    if not password_helper.verify_password(request.password, user.password):
        response.status_code = status.HTTP_403_FORBIDDEN
        return {
            'message': "Invalid email and/or password",
            'status_code': 403,
            'error': "FORBIDDEN"
        }

    # Create access token
    access_token = create_access_token({"sub": str(user.id)})

    # Set token in HTTP-only cookie
    response.set_cookie(key="user_access_token", value=access_token, httponly=True)

    return {
        'user_access_token': access_token,
        'email': user.email,
        'name': user.name,
        'id': user.id
    }
