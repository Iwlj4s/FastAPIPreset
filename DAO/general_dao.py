from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from typing import List, Optional, Any, Type

from database import models, schema
from helpers import exception_helper

class GeneralDAO:
    """
    General Data Access Object with common database operations.
    Provides reusable methods for basic CRUD operations for ANY model.

    This is a universal DAO that can work with:
    - User model
    - Item model  
    - Any other future models

    Usage Example:
    ---------------
    **Get all users** 
    - users = await GeneralDAO.get_all_records(db, models.User)
    
    **Update any record**
    - updated_user = await GeneralDAO.update_record(user, user_update_data, db)
    """
    @classmethod
    async def get_all_records(cls, 
                              db: AsyncSession, 
                              model: Type[Any]) -> List[Any]:
        """
        Retrieve all records of specified model from database.
        Works with ANY SQLAlchemy model (User, Item, etc.)
        
        :param db:  AsyncSession
                    Database session for executing queries
        :param model:Type[Any]: SQLAlchemy model class (e.g., models.User, models.Item)
        :return: List[Any] List of all found records of the specified model

        Usage Example:
        ---------------
        **Get all users** 
        - items = await GeneralDAO.get_all_records(db, models.Item)
    
        **Update any record**
        - users = await GeneralDAO.get_all_records(db, models.User)
        """
        query = select(model)
        result = await db.execute(query)

        return result.scalars().all()

    @classmethod
    async def get_record_by_id(cls, 
                               record_id: int,
                               model: Type[Any], 
                               db: AsyncSession) -> Optional[Any]:
        """
        Retrieve single record of specified model from database by its ID.
        Works with ANY SQLAlchemy model.
        
        :param db:  AsyncSession
                    Database session for executing queries
        :param model:Type[Any]: SQLAlchemy model class (e.g., models.User, models.Item)
        :param record_id:   int
                            ID of the record to find in database
        :return:    Optional[Any] 
                    Found record object or None if not found

        Usage Example:
        ---------------
        **Get all users** 
        - user = await GeneralDAO.get_record_by_id(db, models.User, 1)
        """
        query = select(model).where(model.id == int(record_id))
        result = await db.execute(query)

        return result.scalars().first()
    
    @classmethod
    async def update_record(cls,
                            record: Any,
                            update_data: Any,
                            db: AsyncSession) -> Any:
        """
        Update ANY database record with provided data.
        Universal method for all models that supports partial updates.
        
        :param db:  AsyncSession
                    Database session for executing queries
        :param update_data:   Any 
                        Pydantic schema with update data (e.g., ItemUpdate, UserUpdate)        
        :param record:  Any
                        Database record object to update (User instance, Item instance, etc.)
        :return:    Any 
                    Updated record object from database

        How it works:
        ---------------
        1. Converts Pydantic model to dictionary, excluding unset fields
        2. Applies each field update to the database record
        3. Commits changes to database
        4. Refreshes the record from database

        Usage Example:
        ---------------
        **Get all users** 
        - updated_item = await GeneralDAO.update_record(item, item_update_data, db)
        """
        # Convert Pydantic model to dictionary, excluding unset fields
        # This allows partial updates - only provided fields will be updated
        update_data = update_data.dict(exclude_unset=True)

        # Apply all updates to the record using reflection
        for field, value in update_data.items():
            setattr(record, field, value)

        # Commit changes and refresh updated record
        await db.commit()
        await db.refresh(record)

        return record
        
