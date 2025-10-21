from sqlalchemy import select, update, delete, and_, func

from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User


class UserDAO:
    """
    Data Access Object for User model.
    Contains user-specific database operations.
    """
    @classmethod
    async def get_user_email(cls, 
                             db: AsyncSession, 
                             user_email: str):
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
                            user_name: str):
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
                             user_id: int):
        """
        Find user by ID.
        
        :param db: Database session
        :param user_id: User ID to find
        :return: User object or None
        """
        query = select(User).where(User.id == user_id)
        user = await db.execute(query)

        return user
