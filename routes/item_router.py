from fastapi import Depends, APIRouter, Response

from sqlalchemy.ext.asyncio import AsyncSession

from database import schema
from database.database import get_db

from repository import item_repository
from repository.user_repository import get_current_user


"""
Item API routes.
Defines REST endpoints for item-related operations.
"""

# Router configuration with prefix and tags for Swagger documentation
item_router = APIRouter(
    prefix="/items",    # All routes will be prefixed with /items/API
    tags=["item_router"] # Grouped under "Items" in Swagger UI
)

@item_router.post("/create_item")
async def add_item(request: schema.Item,
                   current_user: schema.User = Depends(get_current_user),
                   db: AsyncSession = Depends(get_db)):
    """
    Create a new item for the authenticated user.
    
    - **request**: Item creation data (name)
    - **current_user**: Automatically injected authenticated user
    - **db**: Database session dependency
    
    Returns created item data with success message.
    """

    return await item_repository.create_item(request=request,
                                             current_user=current_user, 
                                             db=db)

@item_router.post("/delete_item/{item_id}")
async def delete_item(item_id: int,
                      current_user: schema.User = Depends(get_current_user),
                      db: AsyncSession = Depends(get_db)):
    """
    Delete a specific item (only if owned by current user).
    
    - **item_id**: ID of item to delete (path parameter)
    - **current_user**: Authenticated user for ownership verification
    
    Returns success message upon deletion.
    """
    return await item_repository.delete_item(db=db, item_id=item_id, user_id=current_user.id)


@item_router.get("/item/{item_id}")
async def get_item(item_id: int,
                   db: AsyncSession = Depends(get_db)):
    """
    Retrieve a specific item by ID.
    No authentication required - public access.
    
    - **item_id**: ID of item to retrieve (path parameter)
    
    Returns item data.
    """
    return await item_repository.show_item(item_id=int(item_id),
                                           db=db)

@item_router.get("/")
async def get_items_list(db: AsyncSession = Depends(get_db)):
    """
    Retrieve all items from the system with user information.
    Public endpoint - no authentication required.
    
    Returns list of all items with user details.
    """
    items_list = await item_repository.get_all_items(db=db)
    return items_list