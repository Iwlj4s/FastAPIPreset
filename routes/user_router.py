from fastapi import Depends, APIRouter, Response

from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from database.schema import User
from database import schema, models
from helpers.general_helper import CheckHTTP404NotFound

from repository.user_repository import get_current_user
from repository import user_repository

from DAO.general_dao import GeneralDAO

user_router = APIRouter(
    prefix="/users/API",
    tags=["users"]
)


@user_router.post("/sign_up", status_code=201, tags=["users"])
async def sign_up(request: schema.User,
                  response: Response,
                  db: AsyncSession = Depends(get_db)):
    return await user_repository.sign_up(request, response, db)


@user_router.post("/sign_in", status_code=200, tags=["users"])
async def sign_in(request: schema.UserSignIn,
                  response: Response,
                  db: AsyncSession = Depends(get_db)):
    return await user_repository.login(request, response, db)


@user_router.post("/logout", tags=["users"])
async def logout(response: Response):
    response.delete_cookie(key='user_access_token')
    return {'message': 'Пользователь успешно вышел из системы'}


@user_router.get("/me/", status_code=200, tags=["users"])
async def get_me(response: Response,
                 user_data: User = Depends(get_current_user)):
    return user_data


@user_router.post("/user/{user_id}", status_code=200, tags=["users"])
async def get_user(user_id: int,
                   db: AsyncSession = Depends(get_db)):
    user = await GeneralDAO.get_item_by_id(db=db, item=models.User, item_id=int(user_id))
    CheckHTTP404NotFound(founding_item=user, text="Пользователь не найден")
    return {
        'user_id:': user.id,
        'user_name:': user.name,
        'user_email': user.email,
        'somethings': user.something
    }


@user_router.get("/users_list")
async def get_users_for_user(db: AsyncSession = Depends(get_db)):
    users = await GeneralDAO.get_all_items(db=db, item=models.User)
    CheckHTTP404NotFound(founding_item=users, text="Пользователи не найдены")
    users_list = []
    for user in users:
        users_list.append({
            'id': user.id,
            'title': user.name,
            'user_email': user.email,
            'somethings': user.something
        })
    return users_list


@user_router.get("/me/somethings", status_code=200, tags=["users"])
async def get_current_user_somethings(current_user: schema.User = Depends(get_current_user),
                                      db: AsyncSession = Depends(get_db)):
    return await user_repository.get_current_user_somethings(current_user=current_user, db=db)


@user_router.get("/me/{something_id}", status_code=200, tags=["users"])
async def get_current_user_somethings(something_id: int,
                                      response: Response,
                                      current_user: schema.User = Depends(get_current_user),
                                      db: AsyncSession = Depends(get_db)):
    return await user_repository.get_current_user_something(something_id=something_id,
                                                            current_user=current_user,
                                                            response=response,
                                                            db=db)
