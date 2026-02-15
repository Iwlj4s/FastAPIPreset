from sqlalchemy import select, update, delete, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from typing import List, Optional

from DAO.general_dao import GeneralDAO
from database import response_schemas
from database import models
from helpers import exception_helper
from services.user_services import UserService


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
        await exception_helper.CheckHTTP404NotFound(founding_item=user, text="User not found")
        
        user_with_items = await UserService.create_user_with_items_response(user=user)

        return user_with_items
    
    @classmethod
    async def get_all_users(cls,
                            db: AsyncSession) -> response_schemas.UserResponse:
        """
        Get all users from database and return formatted response.
        Delegates formatting to UserService.
        
        :param db: Database session
        :return: List[response_schemas.UserResponse] - List of formatted user responses
        """

        # Get all users from DB
        users = await GeneralDAO.get_all_records(db=db, model=models.User)
        await exception_helper.CheckHTTP404NotFound(founding_item=users, text="Users not found")
        
        # Delegate formatting to UserService to separate concerns
        users_list = await UserService.get_formated_users(users=users)

        return users_list