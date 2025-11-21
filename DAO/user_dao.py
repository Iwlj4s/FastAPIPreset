from sqlalchemy import select, update, delete, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from typing import List, Optional

from database import response_schemas
from database.models import User
from helpers import general_helper


class UserDAO:
    """
    Data Access Object for User model.
    Contains user-specific database operations.
    """
    @classmethod
    async def get_user_email(cls, 
                             db: AsyncSession, 
                             user_email: str) -> Optional[User]:
        """
        Find user by email address.
        
        :param db: Database session
        :param user_email: Email to search for
        :return: User object or None
        """
        query = select(User).where(User.email == str(user_email))
        email = await db.execute(query)

        return email.scalars().first()

    @classmethod
    async def get_user_name(cls, 
                            db: AsyncSession, 
                            user_name: str) -> Optional[User]:
        """
        Find user by username.
        
        :param db: Database session
        :param user_name: Username to search for
        :return: User object or None
        """
        query = select(User).where(User.name == str(user_name))
        name = await db.execute(query)

        return name.scalars().first()

    @classmethod
    async def get_user_by_id(cls, 
                             db: AsyncSession, 
                             user_id: int) -> Optional[User]:
        """
        Find user by ID.
        
        :param db: Database session
        :param user_id: User ID to find
        :return: User object or None
        """
        query = select(User).where(User.id == user_id)
        result = await db.execute(query)

        user = result.scalars().first()

        return user

    @classmethod
    async def get_user_with_items(cls, 
                                  user_id: int,
                                  db: AsyncSession) -> response_schemas.UserWithItemsResponse:
        """
            Find user with items by user's ID.
            
            :param db: Database session
            :param user_id: User ID to find
            :return: User data
        """
        user = await cls.get_user_by_id(user_id=user_id, db=db)
        await general_helper.CheckHTTP404NotFound(founding_item=user, text="User not found")

        user_data = response_schemas.UserWithItemsResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            items=[
                response_schemas.ItemResponse(
                    id=item.id,
                    name=item.name,
                    description=item.description,
                    user_id=item.user_id
                )
                for item in user.item
            ]
        )

        return user_data