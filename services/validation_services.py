from typing import Type, Any, Dict, Optional
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from database import models


class ValidationService:
    """
    Service for validating model data based on predefined rules
    
    This service provides:
    - Global field uniqueness validation (across entire database)
    - Per-user field uniqueness validation (unique within a single user)
    - Centralized validation rule management through the VALIDATION_RULES dictionary
    
    Rules can be easily extended without changing validation logic:
    simply add a new model or field to VALIDATION_RULES.
    
    Usage example in routes:
        await ValidationService.validate_update(
            model_class=Item,
            record=existing_item,
            update_data={"name": "new_name"},
            db=db_session
        )
    
    If a duplicate record is found during validation, HTTPException(409) is raised.
    """

    VALIDATION_RULES = {
        "User": {
            "unique_fields": ["email", "name"],
            "required_fields": ["email", "name", "password"]
        },

        "Item": {
            "unique_fields": [],
            "required_fields": ["name", "user_id"],
            "unique_per_user_fields": ["name"]
        }
    }

    """
    Dictionary with validation rules for each model.
    
    Structure:
        "ModelName": {
            "unique_fields": [...],              # Globally unique fields (across entire DB)
            "required_fields": [...],            # Required fields
            "unique_per_user_fields": [...]      # Unique within a single user
        }
    
    Field types:
    - unique_fields: Field must be unique across the entire table.
                    Example: email, username.
                    Check: no two records with the same value.
    
    - required_fields: Field cannot be None/empty.
                      Used when creating a new record.
                      (Not implemented in this file, see repositories)
    
    - unique_per_user_fields: Field must be unique for a specific user.
                             Example: project name, folder name.
                             Check: no two records with the same value AND the same user_id.
                             !Requires user_id attribute in the model!
    """

    @classmethod
    def get_validation_rules(cls, model_class: Type) -> Dict[str, Any]:
        """
        Get validation rules for the specified model class.
        
        This is a sync helper method that doesn't require database access.
        Used to retrieve the configuration before validation.
        
        Args:
            model_class (Type): SQLAlchemy model class (e.g., User, Item).
                               The class name is used as a key in VALIDATION_RULES.
        
        Returns:
            Dict[str, Any]: Dictionary with validation rules for the model.
                           If the model is not found in the rules, returns an empty dictionary {}.
        
        Example:
            rules = ValidationService.get_validation_rules(Item)
            # Returns: {
            #     "unique_fields": [],
            #     "required_fields": ["name", "user_id"],
            #     "unique_per_user_fields": ["name"]
            # }
        """
        # Magic method to get class name
        model_name = model_class.__name__
        
        # Return the rules dictionary for the model, or empty dict if not found
        return cls.VALIDATION_RULES.get(model_name, {})
    
    @classmethod
    async def check_field_duplicates(cls,
                                     field: str,
                                     value: Any,
                                     model: Type,
                                     current_record_id: Optional[int],
                                     db: AsyncSession) -> bool:
        """
        Check if a field value is duplicated in the database (globally).
        
        Searches for records in the table where the specified field has the given value.
        If current_record_id is provided, excludes the current record from the check
        (needed for updating a record with its own old value).
        
        Args:
            field (str): Name of the field to check (e.g., "email", "name").
            value (Any): Value to search for. If None, the check is skipped
                        (see validate_update).
            model (Type): SQLAlchemy model class for the query (Item, User, etc.).
            current_record_id (Optional[int]): ID of the current record being edited.
                                              If provided, this record is excluded from the check.
                                              If None, all records in the table are checked.
            db (AsyncSession): Async SQLAlchemy session for database access.
        
        Returns:
            bool: True if a duplicate value is found (conflict),
                  False if no duplicates exist (safe to update).
        
        Example:
            # Check if a user with email "test@example.com" already exists
            exists = await ValidationService.check_field_duplicates(
                field="email",
                value="test@example.com",
                model=User,
                current_record_id=None,  # Check all User records
                db=db_session
            )
            if exists:
                # Email is already used by another user!
        
        Internally uses SQLAlchemy exists() for efficient checking
        (doesn't load the actual record, only checks for existence).
        """
        # Build the base query to check for existence of the value in the field 
        query = select(exists().where(getattr(model, field) == value))
        # Exclude the current record if updating
        if current_record_id is not None:
            query = query.where(model.id != current_record_id)
        
        result = await db.execute(query)
        return result.scalar()

    @classmethod
    async def validate_update(cls,
                              model_class: Type,
                              record: Any,
                              update_data: dict,
                              db: AsyncSession) -> None:
        """
        Main validation method for update data of a record.
        
        This method checks all types of duplicates according to VALIDATION_RULES:
        1. Globally unique fields (unique_fields)
        2. Per-user unique fields (unique_per_user_fields)
        
        If a duplicate conflict is found, raises HTTPException(409).
        
        Args:
            model_class (Type): Model class for validation (Item, User, etc.).
                               Rules are retrieved from VALIDATION_RULES using the class name.
            record (Any): Instance of the current record being edited from the database.
                         Used to exclude the current record from checks
                         and to get user_id for per-user checks.
            update_data (dict): Dictionary with update data (usually from request body).
                               Keys = field names, values = new values.
                               Only fields present in this dictionary are checked!
                               !If a field is not in update_data, it is not validated!
            db (AsyncSession): Async SQLAlchemy session for database access.
        
        Raises:
            HTTPException(status_code=409): If a duplicate value is found.
                Contains detailed error message:
                - For global unique: "Value '...' for field '...' already exists"
                - For per-user unique: "Value '...' for field '...' already exists for this user"
        
        Returns:
            None: If validation succeeds, raises nothing.
        
        Usage examples:
        
            # Example 1: updating an Item
            item = await ItemRepository.get_item_by_id(1, db)
            try:
                await ValidationService.validate_update(
                    model_class=Item,
                    record=item,
                    update_data={"name": "new name", "description": "new desc"},
                    db=db
                )
                # Validation passed, can update
                await ItemRepository.update_item(item, update_data, db)
            except HTTPException as e:
                # Handle duplicate error
                raise e
        
            # Example 2: updating a User (email)
            user = await UserRepository.get_user_by_id(1, db)
            try:
                await ValidationService.validate_update(
                    model_class=User,
                    record=user,
                    update_data={"email": "newemail@example.com"},
                    db=db
                )
            except HTTPException as e:
                # Email is already in use
                raise
        
        Workflow:
        1. Gets validation rules for the model via get_validation_rules()
        2. Checks globally unique fields (unique_fields):
           - For each field in update_data that exists in unique_fields
           - Calls check_field_duplicates()
           - If duplicate found -> HTTPException(409)
        
        3. Checks per-user unique fields (unique_per_user_fields):
           - For each field in update_data that exists in unique_per_user_fields
           - Skips if value == None
           - Calls check_field_duplicates_per_user()
           - If duplicate found -> HTTPException(409)
        
        Adding new validations:
            For a new model with per-user fields, simply update VALIDATION_RULES:
            
            "MyModel": {
                "unique_fields": ["code"],
                "unique_per_user_fields": ["name", "slug", "description"]
            }
            
            No other changes needed! validate_update() will handle everything automatically.
        """
        rules = cls.get_validation_rules(model_class)
        unique_fields = rules.get("unique_fields", [])

        # Global check for unique fields - ONLY fields that are being updated
        for field in unique_fields:
            # Check ONLY fields present in update_data (fields being changed)
            if field in update_data:
                value = update_data[field]
                if value is not None:
                    is_duplicate = await cls.check_field_duplicates(
                        field=field,
                        value=value,
                        model=model_class,
                        current_record_id=record.id if hasattr(record, 'id') else None,
                        db=db,
                    )
                    if is_duplicate:
                        raise HTTPException(
                            status_code=409,
                            detail=f"Value '{value}' for field '{field}' already exists",
                        )

        # Per-user check for unique fields - ONLY fields that are being updated
        if "unique_per_user_fields" in rules:
            for field in rules["unique_per_user_fields"]:
                # Check ONLY fields present in update_data (fields being changed)
                if field in update_data:
                    value = update_data[field]
                    if value is None:
                        continue
                    
                    is_duplicate = await cls.check_field_duplicates_per_user(
                        field=field,
                        value=value,
                        model=model_class,
                        record=record,
                        db=db,
                    )
                    if is_duplicate:
                        raise HTTPException(
                            status_code=409,
                            detail=f"Value '{value}' for field '{field}' already exists for this user",
                        )

    @classmethod
    async def check_field_duplicates_per_user(cls,
                                              field: str,
                                              value: Any,
                                              model: Type,
                                              record: Any,
                                              db: AsyncSession) -> bool:
        """
        Check if a field value is duplicated within a single user's records.
        
        Searches for records in the table where:
        1. The specified field has the given value
        2. user_id matches the current record's user_id
        3. Excludes the current record itself (by ID)
        
        This method is UNIVERSAL - it works with any field and any model
        that has user_id and id attributes.
        
        Args:
            field (str): Name of the field to check (e.g., "name", "code", "slug").
            value (Any): Value to search for.
            model (Type): SQLAlchemy model class (Item, Project, Folder, etc.).
            record (Any): Instance of the current record being edited.
                         user_id and id are extracted from this record to exclude it from search.
                         Requires attributes: user_id and id.
            db (AsyncSession): Async SQLAlchemy session for database access.
        
        Returns:
            bool: True if a duplicate value is found for this user,
                  False if no duplicates exist (safe to update).
        
        Error handling:
            Does not raise exceptions itself. HTTPException is raised by validate_update().
        """
        # Get user_id from the current record
        user_id = getattr(record, 'user_id', None)
        if user_id is None:
            return False
        
        # Build the query to check for existence of the value for this user
        query = select(exists().where(
            (getattr(model, field) == value) &
            (model.user_id == user_id)
        ))
        
        # Exclude the current record by ID
        if hasattr(record, 'id') and record.id:
            query = query.where(model.id != record.id)
        
        result = await db.execute(query)
        return result.scalar()