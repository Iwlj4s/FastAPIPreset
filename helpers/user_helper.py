from fastapi import Request, HTTPException, status, Depends
from starlette.responses import Response

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database import shema
from database.database import get_db


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


async def get_user(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    user_email = request.session.get('user')
    if not user_email:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    user = await ... # get by email

    if not user:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    return user
