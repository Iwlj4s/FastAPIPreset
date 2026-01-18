from starlette.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any

from DAO.user_dao import UserDAO
from database import response_schemas, schema
from helpers import password_helper
from helpers.exception_helper import CheckHTTP403FORBIDDEN_BOOL, CheckHTTP404NotFound
from helpers.jwt_helper import create_access_token


"""
User authentication helper functions.
Handles login process and token generation.
"""


async def take_access_token_for_user(db: AsyncSession, 
                                     response: Response, 
                                     request: schema.UserSignIn) -> response_schemas.CurrentUserResponse:
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
    await CheckHTTP404NotFound(user, "User not found")

    is_password_valid = password_helper.verify_password(request.password, user.password)

    # Verify password
    print(f"   Verifying password...")
    await CheckHTTP403FORBIDDEN_BOOL(
        not is_password_valid,
        "Invalid email and/or password"
    )

    # Create access token
    access_token = create_access_token({"sub": str(user.id)})

    # Set token in HTTP-only cookie
    response.set_cookie(key="user_access_token", 
                        value=access_token, 
                        httponly=True)

    return response_schemas.CurrentUserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        bio=user.bio,
        user_access_token=access_token
    )
