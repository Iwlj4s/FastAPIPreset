from sqlalchemy import select, update, delete, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from typing import List, Optional

from DAO.general_dao import GeneralDAO
from database import response_schemas
from database import models
from helpers import general_helper


class UserDAO:
    """
    Data Access Object for User model.
    Contains user-specific database operations.
    """
    @classmethod
    async def get_user_email(cls, 
                             db: AsyncSession, 
                             user_email: str) -> Optional[models.User]:
        """
        Find user by email address.
        
        :param db: Database session
        :param user_email: Email to search for
        :return: User object or None
        """
        query = select(models.User).where(models.User.email == str(user_email))
        email = await db.execute(query)

        return email.scalars().first()

    @classmethod
    async def get_user_name(cls, 
                            db: AsyncSession, 
                            user_name: str) -> Optional[models.User]:
        """
        Find user by username.
        
        :param db: Database session
        :param user_name: Username to search for
        :return: User object or None
        """
        query = select(models.User).where(models.User.name == str(user_name))
        name = await db.execute(query)

        return name.scalars().first()

    @classmethod
    async def get_user_by_id(cls, 
                             db: AsyncSession, 
                             user_id: int) -> Optional[models.User]:
        """
        Find user by ID.
        
        :param db: Database session
        :param user_id: User ID to find
        :return: User object or None
        """
        query = select(models.User).where(models.User.id == user_id)
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
            bio=user.bio,
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
    
    @classmethod
    async def get_all_users(cls,
                            db: AsyncSession) -> response_schemas.UserResponse:
        # Get all users
        users = await GeneralDAO.get_all_records(db=db, model=models.User)
        await general_helper.CheckHTTP404NotFound(founding_item=users, text="Users not found")
        
        # Format response with user items (For now this will be here, I'll move it)
        # Use Response Schema to avoid recursion
        users_list = []
        for user in users:
            user_data = response_schemas.UserResponse(
                id=user.id,
                name=user.name,
                email=user.email,
                bio=user.bio,
            )
            users_list.append(user_data)

        return users_list