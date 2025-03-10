from starlette.responses import Response

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from DAO.user_dao import UserDAO
from database import schema
from helpers import password_helper
from helpers.jwt_helper import create_access_token


async def take_access_token_for_user(db: AsyncSession, response: Response, request: schema.UserSignIn):
    user = await UserDAO.get_user_email(db=db, user_email=str(request.email))
    if not user:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {
            'message': "Invalid email and/or password",
            'status_code': 403,
            'error': "FORBIDDEN"
        }

    if not password_helper.verify_password(request.password, user.password):
        response.status_code = status.HTTP_403_FORBIDDEN
        return {
            'message': "Invalid email and/or password",
            'status_code': 403,
            'error': "FORBIDDEN"
        }

    # Creating access token #
    access_token = create_access_token({"sub": str(user.id)})
    # Write access token in cookie #
    response.set_cookie(key="user_access_token", value=access_token, httponly=True)

    return {
        'user_access_token': access_token,
        'email': user.email,
        'name': user.name,
        'id': user.id
    }
