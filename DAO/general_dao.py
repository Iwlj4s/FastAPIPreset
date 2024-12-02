from sqlalchemy import select, update, delete, and_, func, desc

from sqlalchemy.ext.asyncio import AsyncSession


class GeneralDAO:
    @classmethod
    async def get_all_items(cls, db: AsyncSession, item):
        """
        :param db: database
        :param item: Founding item, like models.User
        :return: Founded items
        """
        query = select(item)
        items = await db.execute(query)

        return items.scalars().all()

    @classmethod
    async def get_item_by_id(cls, db: AsyncSession, item, item_id: int):
        query = select(item).where(item.id == int(item_id))
        item = await db.execute(query)

        return item.scalars().first()
