from pydantic import BaseModel, Field

from typing import Union, Optional

"""
Pydantic schemas for data validation and serialization.
Used for request/response data modeling.
"""

class Item(BaseModel):
    """Schema for item creation and validation"""
    name: Union[str, None] = Field(default=None, min_length=3, title="Item name")
    description: Optional[str] = Field(default=None, min_length=3, title="Item description")

class ItemUpdate(BaseModel):
    """Schema for update item """
    name: Optional[str] = None
    description: Optional[str] = None

class User(BaseModel):
    """Schema for user registration and validation"""
    name: Union[str, None] = Field(default=None, min_length=3, title="User name")
    email: Union[str, None] = Field(default=None, title="User's email")
    password: Union[str, None] = Field(default=None, min_length=4, title="User's password")
    bio: Optional[str] = Field(default=None, min_length=10, title="User's biography")

class UserSignIn(BaseModel):
    """Schema for user login authentication"""
    email: Union[str, None] = Field(default=None, title="User's email")
    password: Union[str, None] = Field(default=None, min_length=4, title="User's password")

class UserUpdate(BaseModel):
    """Schema for update user"""
    name: Union[str, None] = Field(default=None, min_length=3, title="User name")
    email: Union[str, None] = Field(default=None, title="User's email")
    bio: Optional[str] = Field(default=None, min_length=10, title="User's biography")
