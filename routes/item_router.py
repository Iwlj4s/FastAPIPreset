from fastapi import Depends, APIRouter, Response
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, List


from context.request_context import RequestContext, get_request_context
from database import response_schemas, schema
from database.database import get_db

from repository import item_repository
from repository.user_repository import get_current_user


"""
ITEM API ROUTES

Defines REST endpoints for item-related operations.
This module handles HTTP requests and responses for items.

Architecture:
-------------
HTTP Request → FastAPI Route → Item Repository → Business Logic

Each endpoint:
1. Receives HTTP request
2. Extracts parameters and data  
3. Calls appropriate repository function
4. Returns standardized HTTP response
"""

# Router configuration with prefix and tags for Swagger documentation
item_router = APIRouter(
    prefix="/items",    # All routes will be prefixed with /items/API
    tags=["item_router"] # Grouped under "Items" in Swagger UI
)


@item_router.get("/")
async def get_items_list(db: AsyncSession = Depends(get_db)) -> response_schemas.ItemListResponse:
    """
    Retrieve all items from the system with user information.
    Public endpoint - no authentication required.
    
    Returns list of all items with user details in standardized format.
    """
    items_list = await item_repository.get_all_items(db=db)
    return items_list


@item_router.get("/item/{item_id}")
async def get_item(item_id: int,
                   db: AsyncSession = Depends(get_db)) -> response_schemas.ItemDetailResponse:
    """
    Retrieve a specific item by ID with user information.
    No authentication required - public access.
    
    - **item_id**: ID of item to retrieve (path parameter)
    
    Returns item data with user information in standardized format.
    """
    return await item_repository.show_item(item_id=int(item_id),
                                           db=db)


@item_router.post("/create_item")
async def add_item(request: schema.Item,
                   request_context: RequestContext = Depends(get_request_context)) -> response_schemas.ItemCreateResponse:
    """
    Create a new item for the authenticated user.
    Requires valid JWT authentication.
    
    - **request**:  schema.Item
                    Item creation data with name and optional description

    - **request_context**: Request Context which use basic stuff:
        - **current_user**: Automatically injected authenticated user
        - **db**: Database session dependency
    
    Returns created item data in standardized format.
    """

    return await item_repository.create_item(request=request,
                                             current_user=request_context.current_user, 
                                             db=request_context.db)

@item_router.patch("/update_item/{item_id}", status_code=200)
async def get_me(item_id: int,
                 item_data: schema.ItemUpdate,
                 request_context: RequestContext = Depends(get_request_context)) -> response_schemas.ItemUpdateResponse:
    """
    Update current user's item using PATCH method.
    Requires valid JWT token and item ownership.

    - **item_id**:  int 
                    ID of the item to update

    - **item_data**:    schema.ItemUpdate
                        Update data with optional name and/or description

    - **request_context**: Request Context which use basic stuff:
        - **current_user**: Automatically injected authenticated user
        - **db**: Database session dependency
        
    Returns updated item data in standardized format.
    """

    return await item_repository.update_item(item_id=item_id,
                                             user_id=request_context.current_user.id,
                                             item_data=item_data,
                                             db=request_context.db)

@item_router.delete("/delete_item/{item_id}")
async def delete_item(item_id: int,
                      request_context: RequestContext = Depends(get_request_context)) -> response_schemas.ItemDeleteResponse:
    """
    Delete a specific item (only if owned by current user).
    Requires valid JWT token and item ownership.
    
    - **item_id**:  int (path parameter)
                    ID of the item to delete

    - **request_context**: Request Context which use basic stuff:
        - **current_user**: Automatically injected authenticated user
        - **db**: Database session dependency
    
    Returns success message in standardized format.
    """
    return await item_repository.delete_item(item_id=item_id, 
                                             user_id=request_context.current_user.id,
                                             db=request_context.db)
