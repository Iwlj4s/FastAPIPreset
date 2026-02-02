from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, List


from starlette.responses import Response

from database import schema, models, response_schemas

from helpers import exception_helper
from DAO.general_dao import GeneralDAO
from DAO.item_dao import ItemDao
from database.database import get_db

"""
ITEM BUSINESS LOGIC LAYER

This module handles item-related business operations and coordinates 
between API routes and data access layer.

ARCHITECTURE:
-------------
API Routes → Item Repository → DAO (Data Access Objects) → Database

Each function here:
1. Validates business rules
2. Handles errors  
3. Transforms data between layers
4. Returns standardized responses
"""

async def create_item(request: schema.Item,
                      current_user: schema.User,
                      db: AsyncSession = Depends(get_db)) -> response_schemas.ItemCreateResponse:
    
    """
    Create a new item for the current user.
    Validates item name uniqueness for the user before creation.
    
    :param request: schema.Item
                    Item creation data with name and optional description

    :param current_user:    schema.User  
                            Authenticated user creating the item

    :param db:  AsyncSession
                Database session for operations

    :return:    ItemCreateResponse
                Standardized response with created item data

    :raises:    HTTPException 409
                If user already has item with same name
    """
    # Check if user already has an item with the same name
    user_item = await ItemDao.get_item_by_user_id_and_item_name(db=db, 
                                                                user_id=current_user.id, 
                                                                item_name=request.name)
    # Raise conflict error if duplicate name found
    await exception_helper.CheckHTTP409Conflict(founding_item=user_item, 
                                              text="You already have an item with this name")
    # Create new item
    new_item = await ItemDao.create_item(db=db,
                                         request=request,
                                         user_id=current_user.id)
    await db.refresh(new_item)

    return response_schemas.ItemCreateResponse(
        message="Item has been created successfully",
        status_code=200,
        data=response_schemas.ItemResponse(
            id=new_item.id,
            name=new_item.name,
            description=new_item.description,
            user_id=new_item.user_id
        )
    )

async def update_item(item_id: int,
                      user_id: int,
                      item_data: schema.ItemUpdate,
                      db: AsyncSession) -> response_schemas.ItemUpdateResponse:
    
    """
    Update item with comprehensive validation and ownership check.
    Supports partial updates - only provided fields will be updated.
    
    :param item_id: int
                    ID of the item to update

    :param user_id: int  
                    ID of user attempting update (for ownership verification)
    
    :param item_data:   schema.ItemUpdate
                        Update data with optional name and/or description

    :param db:  AsyncSession
                Database session for operations

    :return:    ItemUpdateResponse
                Standardized response with created item data

    :raises:    HTTPException 400
                If no fields provided for update

                HTTPException 404  
                If item not found or user doesn't own it

                HTTPException 409
                If new name conflicts with existing item
    """

    if not item_data.dict(exclude_unset=True):
        raise HTTPException(status_code=400, detail="No fields to update")
    
    item = await ItemDao.get_item_by_user_id(db=db, 
                                            item_id=item_id, 
                                            user_id=user_id)
    
    await exception_helper.CheckHTTP404NotFound(founding_item=item, 
                                              text="Item not found or you don't have permission to update it")
    
    updated_item = await GeneralDAO.update_record(model=models.Item,
                                                  record=item,
                                                  update_data=item_data,
                                                  db=db)
    
    return response_schemas.ItemUpdateResponse(
        message="Item has been updated",
        status_code=200,
        data = response_schemas.ItemResponse(
            id=updated_item.id,
            name=updated_item.name,
            description=updated_item.description,
            user_id=updated_item.user_id
        )
    )


async def delete_item(item_id: int,
                      user_id: int,
                      db: AsyncSession) -> response_schemas.ItemDeleteResponse:
    """
    Delete an item with ownership verification.
    Only the item owner can delete their items.
    
    :param item_id: int
                    ID of the item to delete

    :param user_id: int
                    ID of user attempting deletion

    :param db:  AsyncSession
                Database session for operations

    :return:    ItemDeleteResponse
                Standardized success response

    :raises:    HTTPException 404
                If item not found or user doesn't own it
    """
    # Verify item exists and user owns it
    item = await ItemDao.get_item_by_user_id(db=db, 
                                             item_id=item_id, 
                                             user_id=user_id)
    await exception_helper.CheckHTTP404NotFound(founding_item=item, 
                                              text="Item not found or you don't have permission to delete it")

    # Delete the item
    await ItemDao.delete_item(db=db, item_id=item_id, user_id=user_id)

    return response_schemas.ItemDeleteResponse(
        message="Item has been deleted",
        status_code=200
    )


async def show_item(item_id: int,
                    db: AsyncSession = Depends(get_db)) -> response_schemas.ItemDetailResponse:
    """
    Retrieve a specific item by ID with user information.
    No ownership check - any user can view any item.
    
    :param item_id: int
                    ID of the item to delete

    :param db:  AsyncSession
                Database session for operations

    :return:    ItemDetailResponse
                Standardized success response

    :raises:    HTTPException 404
                If item not found
    """
    item = await GeneralDAO.get_record_by_id(record_id=item_id,
                                             model=models.Item,
                                             db=db)
    await exception_helper.CheckHTTP404NotFound(founding_item=item, text="Item not found")
    
    return response_schemas.ItemDetailResponse(
        message="Item retrieved successfully",
        status_code=200,
        data=response_schemas.ItemWithUserResponse(
            id=item.id,
            name=item.name,
            description=item.description,
            user_id=item.user.id,
            user_name=item.user.name,
            user_email=item.user.email
        )
    )

async def get_all_items(db: AsyncSession) -> response_schemas.ItemListResponse:
    """
    Retrieve all items from the system with user information.
    Includes user details for each item.

    :param db:  AsyncSession
                Database session for operations

    :return:    ItemListResponse
                Standardized success response

    :raises:    HTTPException 404
                If items not found
    """

    items_list = await ItemDao.get_all_items(db=db)
    
    return response_schemas.ItemListResponse(
        message="Items retrieved successfully",
        status_code=200,
        data=items_list
    )