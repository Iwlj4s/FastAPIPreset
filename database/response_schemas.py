from pydantic import BaseModel
from typing import List, Optional, Generic, TypeVar

# Type variable for generic types - represents any data type
T = TypeVar('T')

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


class DataResponse(BaseResponse, Generic[T]):
    """
    Generic response schema for single object endpoints.
    Extends BaseResponse with optional data field of any type.
    
    Usage:
    - Single object retrieval (GET /items/{id})
    - Create operations (POST /items)
    - Update operations (PATCH /items/{id})
    
    Generic type T determines the data structure:
    - DataResponse[ItemResponse] for item data
    - DataResponse[UserResponse] for user data
    
    Example Response:
    -----------------
    {
        "message": "Item retrieved successfully",
        "status_code": 200,
        "data": {
            "id": 1,
            "name": "Laptop",
            "description": "Gaming laptop",
            "user_id": 5
        }
    }
    """
    data: Optional[T] = None


class ListResponse(BaseResponse, Generic[T]):
    """
    Generic response schema for list/collection endpoints.
    Extends BaseResponse with data field containing list of objects.
    
    Usage:
    - List operations (GET /items)
    - Bulk operations returning multiple objects
    
    Generic type T determines the structure of list items:
    - ListResponse[ItemWithUserResponse] for items with user info
    - ListResponse[UserResponse] for basic user list
    
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
    data: List[T] = []


# Basic enity schemas (without relationships)
class UserResponse(BaseModel):
    """
    Basic user schema without relationships to avoid recursion.
    Contains essential user information for API responses.
    
    Fields:
    - id: Unique user identifier
    - name: User's display name
    - email: User's email address
    
    Use when you need user data without nested item information.
    """
    id: int
    name: str
    email: str
    
    class Config:
        from_attributes = True


class ItemResponse(BaseModel):
    """
    Basic item schema without relationships to avoid recursion.
    Contains essential item information for API responses.
    
    Fields:
    - id: Unique item identifier
    - name: Item name
    - description: Item description
    - user_id: ID of the user who owns this item
    
    Use when you need item data without nested user information.
    """
    id: int
    name: str
    description: str
    user_id: int
    
    class Config:
        from_attributes = True


# Composite schemas (with relationships)
class UserWithItemsResponse(UserResponse):
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

    items: List[ItemResponse] = []


class ItemWithUserResponse(ItemResponse):
    """
    Extended item schema including owner information.
    Prevents recursion by flattening user data instead of nested object.
    
    Extends ItemResponse with:
    - user_name: Name of the user who owns this item
    - user_email: Email of the user who owns this item
    
    Use when you need item details with basic owner information.
    """
    user_name: str
    user_email: str


ItemCreateResponse = DataResponse[ItemResponse]
"""Response type for item creation endpoints"""

ItemUpdateResponse = DataResponse[ItemResponse]
"""Response type for item update endpoints"""

ItemDeleteResponse = BaseResponse
"""Response type for item deletion endpoints"""

ItemDetailResponse = DataResponse[ItemWithUserResponse]
"""Response type for single item retrieval with user info"""

ItemListResponse = ListResponse[ItemWithUserResponse]
"""Response type for item list retrieval with user info"""

UserWithItemsResponseType = DataResponse[UserWithItemsResponse]
"""Response type for user retrieval with items"""