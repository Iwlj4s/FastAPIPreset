from sqlalchemy import select, update, delete, and_, func, desc

from sqlalchemy.ext.asyncio import AsyncSession

from database import shema
from database import models


class SomethingDao:
    @classmethod
    async def create_something(cls, db: AsyncSession, request: shema.Something):
        new_something = models.Something(
            name=request.name
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
