from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from starlette.responses import Response

from database import schema, models

from helpers import general_helper
from DAO.general_dao import GeneralDAO
from DAO.item_dao import ItemDao
from database.database import get_db

"""
Item business logic layer.
Handles item-related operations and coordinates between routes and DAO.
"""

async def create_item(request: schema.Item,
                      current_user: schema.User,
                      db: AsyncSession = Depends(get_db)):
    
    """
    Create a new item for the current user.
    Validates item name uniqueness for the user before creation.
    
    :param request: Item creation data from schema
    :param response: HTTP response object
    :param current_user: Authenticated user creating the item
    :param db: Database session

    :return: Success response with created item data
    :raises HTTPException: 409 if item name already exists for user
    """
    # Check if user already has an item with the same name
    user_item = await ItemDao.get_item_by_user_id_and_item_name(db=db, 
                                                                user_id=current_user.id, 
                                                                item_name=request.name)
    # Raise conflict error if duplicate name found
    await general_helper.CheckHTTP409Conflict(founding_item=user_item, 
                                              text="You already have an item with this name")
    # Create new item
    new_item = await ItemDao.create_item(db=db,
                                         request=request,
                                         user_id=current_user.id)
    await db.refresh(new_item)

    return {
        "message": "'Item' has been added",
        "status_code": 200,
        "data": {
            "id": new_item.id,
            "name": new_item.name,
            "user_id": new_item.user_id
        }
    }

async def delete_item(item_id: int,
                      user_id: int,
                      db: AsyncSession):
    """
    Delete an item with ownership verification.
    Only the item owner can delete their items.
    
    :param item_id: ID of item to delete
    :param user_id: ID of user attempting deletion
    :param db: Database session
    :return: Success response
    :raises HTTPException: 404 if item not found or user doesn't own it
    """
    # Verify item exists and user owns it
    item = await ItemDao.get_item_by_user_id(db=db, 
                                             item_id=item_id, 
                                             user_id=user_id)
    await general_helper.CheckHTTP404NotFound(founding_item=item, 
                                              text="Item not found or you don't have permission to delete it")

    # Delete the item
    await ItemDao.delete_item(db=db, item_id=item_id, user_id=user_id)

    return {
        "message": "Item deleted successfully",
        "status_code": 200
    }



async def show_item(item_id: int,
                    db: AsyncSession = Depends(get_db)):
    """
    Retrieve a specific item by ID.
    No ownership check - any authenticated user can view any item.
    
    :param item_id: ID of item to retrieve
    :param response: HTTP response object
    :param db: Database session
    :return: Item data
    :raises HTTPException: 404 if item not found
    """
    item = await GeneralDAO.get_item_by_id(db=db, 
                                           item=models.Item, 
                                           item_id=int(item_id))
    await general_helper.CheckHTTP404NotFound(founding_item=item, text="Item not found")
    
    return {
        "message": "Successfull",
        "status_code": 200,
        "data": item
    }

async def get_all_items(db: AsyncSession):
    """
    Retrieve all items from the system with user information.
    Includes user details for each item.
    
    :param db: Database session
    :return: List of all items with user information
    :raises HTTPException: 404 if no items found
    """
    items = await GeneralDAO.get_all_items(db=db, item=models.Item)
    await general_helper.CheckHTTP404NotFound(founding_item=items, text="Items not found")

    # Format response with user information
    items_list = []
    for item in items:
        items_list.append({
            'id': item.id,
            'item_name': item.name,
            'user_id': item.user.id,
            'user_name': item.user.name
        })
    return items_list