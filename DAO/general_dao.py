from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession


class GeneralDAO:
    """
    General Data Access Object with common database operations.
    Provides reusable methods for basic CRUD operations.
    """
    @classmethod
    async def get_all_items(cls, 
                            db: AsyncSession, 
                            item):
        """
        Retrieve all items of specified model from database.
        
        :param db: Database session
        :param item: Model class to query (e.g., models.User)
        :return: List of all found items
        """
        query = select(item)
        items = await db.execute(query)

        return items.scalars().all()

    @classmethod
    async def get_item_by_id(cls, 
                             db: AsyncSession, item, 
                             item_id: int):
        """
        Retrieve single item by it's ID.
        
        :param db: Database session
        :param item: Model class to query
        :param item_id: ID of item to find
        :return: Found item or None
        """
        query = select(item).where(item.id == int(item_id))
        item = await db.execute(query)

        return item.scalars().first()
