from pydantic import BaseModel
from typing import List

"""
Response schemas to avoid recursion in serialization.
Separate from request schemas to break circular dependencies.
"""

class ItemResponse(BaseModel):
    """Schema for item responses without user recursion"""
    id: int
    name: str
    user_id: int
    
    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    """Schema for user responses without item recursion"""
    id: int
    name: str
    email: str
    
    class Config:
        from_attributes = True


class UserWithItemsResponse(BaseModel):
    """Schema for user with items (flattened structure)"""
    id: int
    name: str
    email: str
    items: List[ItemResponse] = []
    
    class Config:
        from_attributes = True


class ItemWithUserResponse(BaseModel):
    """Schema for item with user info (flattened structure)"""
    id: int
    name: str
    user_id: int
    user_name: str
    user_email: str
    
    class Config:
        from_attributes = True