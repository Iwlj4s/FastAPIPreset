from fastapi import HTTPException
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from typing import List, Optional, Any, Type

from database import models, schema
from helpers import exception_helper
from services.validation_services import ValidationService

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
                            model: Any,
                            record: Any,
                            update_data: Any,
                            db: AsyncSession) -> Any:
        """
        Update ANY database record with provided data.
        Universal method for all models that supports partial updates.
        
        :param model: SQLAlchemy model class
        :param record: Database record object to update
        :param update_data: Pydantic schema or dict with update data
        :param db: Database session
        :return: Updated record object
        """
        # Convert Pydantic model to dictionary, excluding unset fields
        if hasattr(update_data, "dict"):
            update_data = update_data.dict(exclude_unset=True)
        elif not isinstance(update_data, dict):
            update_data = dict(update_data)
        
        # Validate update data (ValidationService handles all exceptions internally)
        await ValidationService.validate_update(
            model_class=model,
            record=record,
            update_data=update_data,
            db=db
        )
        
        # Updating
        for field, value in update_data.items():
            setattr(record, field, value)

        try:
            await db.commit()
        except IntegrityError as e:
            # Handle database integrity constraint violations as a safety net
            await db.rollback()
            raise HTTPException(
                status_code=409,
                detail="This value already exists or violates a database constraint"
            )
        
        await db.refresh(record)

        return record
        
