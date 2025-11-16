from sqlalchemy import select, update, delete, and_, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from database import schema
from database import models


class ItemDao:
    """
    Data Access Object for Item model.
    Contains item-specific database operations.
    """
    @classmethod
    async def create_item(cls, 
                          db: AsyncSession, 
                          request: schema.Item, 
                          user_id: int) -> models.Item:
        """
        Create new item in database.
        
        :param db: Database session
        :param request: Item data from schema
        :param user_id: ID of user creating the item
        :return: Created item object
        """
        new_item = models.Item(
            name=request.name,
            user_id=user_id
        )

        print(new_item)

        db.add(new_item)
        await db.commit()

        return new_item
    
    @classmethod
    async def delete_item(cls,
                          item_id: int,
                          user_id: int,
                          db: AsyncSession) -> None:

        """
        Delete item with ownership verification.
        Only item owner can delete their items.
        
        :param db: Database session
        :param item_id: ID of item to delete
        :param user_id: User ID for ownership verification
        """
        query = delete(models.Item).where(
            and_(
                models.Item.id == item_id,
                models.Item.user_id == user_id
            )
        )

        await db.execute(query)

        await db.commit()

    @classmethod
    async def get_item_name(cls, 
                            db: AsyncSession, 
                            item_name: str) -> Optional[models.Item]:
        """
        Find item by name.
        
        :param db: Database session
        :param item_name: Name to search for
        :return: Item object or None
        """
        query = select(models.Item).where(models.Item.name == str(item_name))
        name = await db.execute(query)

        return name.scalars().first()

    @classmethod
    async def get_items_by_user_id(cls, 
                                   db: AsyncSession, 
                                   user_id: int) -> List[models.Item]:
        """
        Get all items belonging to specific user.
        
        :param db: Database session
        :param user_id: User ID to filter items
        :return: List of user's items
        """
        query = select(models.Item).where(models.Item.user_id == user_id)
        items = await db.execute(query)
        return items.scalars().all()

    @classmethod
    async def get_item_by_user_id(cls, db: AsyncSession,
                                  item_id: int,
                                  user_id: int) -> Optional[models.Item]:
        """
        Get specific item with ownership verification.
        
        :param db: Database session
        :param item_id: Item ID to find
        :param user_id: User ID for ownership check
        :return: Item object or None
        """
        query = select(models.Item).where(
            and_(
                models.Item.user_id == user_id,
                models.Item.id == item_id
            )
        )
        item = await db.execute(query)
        return item.scalars().first()
    
    @classmethod
    async def get_item_by_user_id_and_item_name(cls, 
                                            db: AsyncSession,
                                            user_id: int,
                                            item_name: str) -> Optional[models.Item]:
        """
        Find item by name for specific user.
        Used to prevent duplicate item names per user.
        
        :param db: Database session
        :param user_id: User ID to filter
        :param item_name: Item name to search for
        :return: Item object or None
        """
        query = select(models.Item).where(
            models.Item.user_id == user_id,
            models.Item.name == item_name
        )

        result = await db.execute(query)

        return result.scalar_one_or_none()
    