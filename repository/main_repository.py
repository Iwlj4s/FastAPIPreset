from fastapi import Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from starlette import status
from starlette.responses import Response

from database import shema, models

from DAO.general_dao import GeneralDAO
from DAO.something_dao import SomethingDao
from database.database import get_db


async def create_something(request: shema.Something,
                           response: Response,
                           db: AsyncSession = Depends(get_db)):
    name = await SomethingDao.get_something_name(db=db, something_name=request.name)

    if name:
        response.status_code = status.HTTP_409_CONFLICT

        return {
            "message": "Имя уже занято",
            "status_code": 409
        }

    new_something = await SomethingDao.create_something(db=db,
                                                        request=request)
    await db.refresh(new_something)

    return {
        "message": "ЧТо то добавлено",
        "status_code": 200,
        "data": {
            "id": new_something.id,
            "name": new_something.name
        }
    }


async def show_something(something_id: int,
                         response: Response,
                         db: AsyncSession = Depends(get_db)):
    something_item = await GeneralDAO.get_item_by_id(db=db, item=models.Something, item_id=int(something_id))
    if not something_item:
        response.status_code = status.HTTP_404_NOT_FOUND

        return {
            "message": "Такого нет!",
            "status_code": 404
        }

    return {
        "message": "Successful",
        "status_code": 200,
        "data": {something_item}
    }
