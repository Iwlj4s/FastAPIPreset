from pydantic import BaseModel
from typing import List

"""
Response schemas to avoid recursion in serialization.
Separate from request schemas to break circular dependencies.
"""

class BaseResponse(BaseModel):
    """
    Base schema for all API responses.
    Provides consistent structure for all endpoints.
    
    All API responses will have:
    - message: Human-readable result description
    - status_code: HTTP status code
    
    Example Response:
    -----------------
    {
        "message": "Operation completed successfully",
        "status_code": 200
    }
    """
    message: str
    status_code: int
    
    class Config:
        from_attributes = True


# Basic enity schemas (without relationships)
class UserResponse(BaseModel):
    """
    Schema for user responses without item recursion.
    Used when you need basic user data without nested items information.
    
    :param id:  int
                Unique identifier of the user

    :param name:    str
                    Full name of the user
                    
    :param email:   str
                    Email address of the user
    """
    id: int
    name: str
    email: str
    
    class Config:
        from_attributes = True


class ItemResponse(BaseModel):
    """
    Schema for item responses without user recursion.
    Used when you need basic item data without nested user information.
    
    :param id:  int
                Unique identifier of the item

    :param name:    str
                    Name of the item

    :param description: str
                        Description of the item  

    :param user_id: int
                        ID of the user who owns this item 
    """
    id: int
    name: str
    description: str
    user_id: int
    
    class Config:
        from_attributes = True


# Composite schemas (with relationships)
class UserWithItemsResponse(BaseModel):
    """
    Schema for user with items (flattened structure).
    Prevents recursion by including items as basic ItemResponse objects.
    
    :param id:      int
                    Unique identifier of the user

    :param name:    str  
                    Full name of the user

    :param email:   str
                    Email address of the user

    :param items:   List[ItemResponse]
                    List of user's items without nested user data to avoid recursion
    """
    id: int
    name: str
    email: str
    items: List[ItemResponse] = []
    
    class Config:
        from_attributes = True


class ItemWithUserResponse(BaseModel):
    """
    Schema for item with user info (flattened structure).
    Prevents recursion by including user fields directly instead of nested user object.
    
    :param id:          int
                        Unique identifier of the item

    :param name:        str
                        Name of the item

    :param description: str
                        Description of the item

    :param user_id:     int
                        ID of the user who owns this item

    :param user_name:   str
                        Name of the user who owns this item  
                        
    :param user_email:  str
                        Email of the user who owns this item
    """
    id: int
    name: str
    description: str
    user_id: int
    user_name: str
    user_email: str
    
    class Config:
        from_attributes = True


# Item API Response Wrappers
class ItemCreateResponse(BaseResponse):
    """
    Schema for item creation responses.
    Extends BaseResponse with created item data.
    
    Usage:
    ------
    - POST /items/create_item endpoint
    
    Example Response:
    -----------------
    {
        "message": "Item created successfully",
        "status_code": 201,
        "data": {
            "id": 1,
            "name": "Laptop",
            "description": "Super laptop",
            "user_id": 5
        }
    }
    """
    data: ItemResponse


class ItemUpdateResponse(BaseResponse):
    """
    Schema for item update responses.
    Extends BaseResponse with updated item data.
    
    Usage:
    ------
    - PATCH /items/update_item/{item_id} endpoint
    
    Example Response:
    -----------------
    {
        "message": "Item updated successfully", 
        "status_code": 200,
        "data": {
            "id": 1,
            "name": "Updated Laptop",
            "description": "Updated description",
            "user_id": 5
        }
    }
    """
    data: ItemResponse


class ItemDeleteResponse(BaseResponse):
    """
    Schema for item deletion responses.
    Extends BaseResponse without additional data.
    
    Usage:
    ------
    - DELETE /items/delete_item/{item_id} endpoint
    
    Example Response:
    -----------------
    {
        "message": "Item deleted successfully",
        "status_code": 200
    }
    """
    pass


class ItemListResponse(BaseResponse):
    """
    Schema for item list responses.
    Extends BaseResponse with list of items including user information.
    
    Usage:
    ------
    - GET /items/ endpoint
    
    Example Response:
    -----------------
    {
        "message": "Items retrieved successfully",
        "status_code": 200,
        "data": [
            {
                "id": 1,
                "name": "Laptop",
                "description": "Gaming laptop", 
                "user_id": 5,
                "user_name": "John Doe",
                "user_email": "john@example.com"
            }
        ]
    }
    """
    data: List[ItemWithUserResponse]


class ItemDetailResponse(BaseResponse):
    """
    Schema for single item detail responses.
    Extends BaseResponse with single item including user information.
    
    Usage:
    ------
    - GET /items/item/{item_id} endpoint
    
    Example Response:
    ---------------
    {
        "message": "Item retrieved successfully",
        "status_code": 200,
        "data": {
            "id": 1,
            "name": "Laptop",
            "description": "Super laptop",
            "user_id": 5, 
            "user_name": "John Doe",
            "user_email": "john@example.com"
        }
    }
    """
    data: ItemWithUserResponse