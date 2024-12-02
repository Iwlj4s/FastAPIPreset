from fastapi import Depends, APIRouter, Response

from sqlalchemy.ext.asyncio import AsyncSession

from database import shema
from database.database import get_db

from repository import main_repository
from repository.main_repository import create_something, show_something

main_router = APIRouter(
    prefix="/something/API",
    tags=["main router"]
)


@main_router.post("/create_something")
async def add_something(response: Response,
                        request: shema.Something,
                        db: AsyncSession = Depends(get_db)):
    return await main_repository.create_something(request=request, response=response, db=db)


@main_router.get("/get_something/{something_id}")
async def get_something(something_id: int,
                        response: Response,
                        db: AsyncSession = Depends(get_db)):
    return await show_something(something_id=int(something_id),
                                response=response,
                                db=db)
