from fastapi import Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from starlette import status
from starlette.responses import Response

from DAO.something_dao import SomethingDao
from database.database import get_db
from database import models, schema

from helpers import password_helper, user_helper
from helpers.general_helper import CheckHTTP404NotFound, CheckHTTP401Unauthorized
from helpers.token_helper import get_token, verify_token

from DAO.general_dao import GeneralDAO
from DAO.user_dao import UserDAO

from helpers import password_helper


async def sign_up(request: schema.User,
                  response,
                  db: AsyncSession):
    email = await UserDAO.get_user_email(db=db, user_email=str(request.email))
    name = await UserDAO.get_user_name(db=db, user_name=str(request.name))

    if email:
        response.status_code = status.HTTP_409_CONFLICT

        return {
            'message': "Email already exist",
            'status_code': 409,
            'error': "CONFLICT"
        }

    if name:
        response.status_code = status.HTTP_409_CONFLICT

        return {
            'message': "This username already exists",
            'status_code': 409,
            'error': "CONFLICT"
        }

    hash_password = password_helper.hash_password(request.password)
    new_user = models.User(name=request.name, email=request.email, password=hash_password)
    db.add(new_user)

    await db.commit()
    await db.refresh(new_user)

    return {
        'message': "Register successfully",
        'status_code': 201,
        'status': "success",
        'data': {
            'id': new_user.id,
            'name': new_user.name,
            'email': new_user.email
        }
    }


async def login(request: schema.UserSignIn,
                response: Response,
                db: AsyncSession):
    user = await user_helper.take_access_token_for_user(db=db,
                                                        response=response,
                                                        request=request)

    if response.status_code == status.HTTP_403_FORBIDDEN:
        return {
            'message': "Invalid email and/or password",
            'status_code': 403,
            'error': "FORBIDDEN"
        }

    return {
        "user_access_token": user['user_access_token'],
        "email": user['email'],
        "name": user['name'],
        "id": user['id']
    }


async def get_current_user(db: AsyncSession = Depends(get_db),
                           token: str = Depends(get_token)):
    user_id = verify_token(token=token)
    print("user_id in get current user: ", user_id)
    if not user_id:
        return {
            'message': "Token not found",
            'status_code': 401,
        }
    user = await GeneralDAO.get_item_by_id(db=db, item=models.User, item_id=int(user_id))

    return user


async def get_current_user_somethings(current_user: schema.User, db: AsyncSession = Depends(get_db)):
    somethings = await SomethingDao.get_somethings_by_user_id(db=db, user_id=current_user.id)
    await CheckHTTP404NotFound(founding_item=somethings, text="Записи не найдены!")

    return {
        "user_id": current_user.id,
        "user_name": current_user.name,
        "somethings": somethings
    }


async def get_current_user_something(something_id: int,
                                     current_user: schema.User,
                                     response: Response,
                                     db: AsyncSession = Depends(get_db)):
    something = await SomethingDao.get_something_by_user_id(db=db, user_id=current_user.id, something_id=something_id)
    await CheckHTTP404NotFound(founding_item=something, text="Запись не найдена!")

    return {
        "user_id": current_user.id,
        "user_name": current_user.name,
        "something": something
    }
