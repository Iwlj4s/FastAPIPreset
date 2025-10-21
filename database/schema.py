from pydantic import BaseModel, Field

from typing import Union

"""
Pydantic schemas for data validation and serialization.
Used for request/response data modeling.
"""

class Item(BaseModel):
    """Schema for item creation and validation"""
    name: Union[str, None] = Field(default=None, min_length=3, title="Item name")


class User(BaseModel):
    """Schema for user registration and validation"""
    name: Union[str, None] = Field(default=None, min_length=3, title="User name")
    email: Union[str, None] = Field(default=None, title="User's email")
    password: Union[str, None] = Field(default=None, min_length=4, title="User's password")


class UserSignIn(BaseModel):
    """Schema for user login authentication"""
    email: Union[str, None] = Field(default=None, title="User's email")
    password: Union[str, None] = Field(default=None, min_length=4, title="User's password")
