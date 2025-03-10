from sqlalchemy import select, update, delete, and_, func, desc

from sqlalchemy.ext.asyncio import AsyncSession

from database import schema
from database import models


class SomethingDao:
    @classmethod
    async def create_something(cls, db: AsyncSession, request: schema.Something, user_id: int):
        new_something = models.Something(
            name=request.name,
            user_id=user_id
        )

        print(new_something)

        db.add(new_something)
        await db.commit()

        return new_something

    @classmethod
    async def get_something_name(cls, db: AsyncSession, something_name: str):
        query = select(models.Something).where(models.Something.name == str(something_name))
        name = await db.execute(query)

        return name.scalars().first()

    @classmethod
    async def get_somethings_by_user_id(cls, db: AsyncSession, user_id: int):
        query = select(models.Something).where(models.Something.user_id == user_id)
        somethings = await db.execute(query)
        return somethings.scalars().all()

    @classmethod
    async def get_something_by_user_id(cls, db: AsyncSession,
                                       something_id,
                                       user_id: int):
        query = select(models.Something).where(
            and_(
                models.Something.user_id == user_id,
                models.Something.id == something_id
            )
        )
        something = await db.execute(query)
        return something.scalars().first()