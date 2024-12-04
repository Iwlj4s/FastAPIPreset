from fastapi import Request, HTTPException, status, Depends
from starlette.responses import Response

import random

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database import shema


# create user's log in shema
# create orm get user by phone/email ...
async def add_user_in_session(db: AsyncSession, request: Request, response: Response, user_data: shema):
    user = await ...  # get_user_by_phone()

    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            'message': "User not found",
            'status_code': 404,
        }

    # verify password

    request.session['user'] = ...  # user.phone, user.email

    return user


async def get_user(request: Request, response: Response):
    user = request.session.get('user')
    if not user:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            'message': "Unauthorizied",
            'status_code': 401
        }

    return user
