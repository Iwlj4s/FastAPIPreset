from typing import List
from sqlalchemy import String, ForeignKey, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.database import Base


class User(Base):
    """
    System user model.
    Contains basic information and relationship with user's items.
    """
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)  # Unique username
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False) # Unique email
    password: Mapped[str] = mapped_column(String)    # Hashed password

    # One-to-many relationship with Item model
    item: Mapped[List["Item"]] = relationship(
        "Item",
        back_populates="user",   # Back reference
        lazy="selectin" # Load related items with user
    )


class Item(Base):
    """
    Item model.
    Belongs to specific user through many-to-one relationship.
    Each user can create an item with the same name as another user
    But user cannot create an item with the same name as another of THEIR items.
    """
    __tablename__ = 'item'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)    # Item name (not unique)
    description: Mapped[str] = mapped_column(String, 
                                             nullable=False, 
                                             server_default="No description") # Item description 
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))    # Foreign key to user

    # Many-to-one relationship with User model
    user: Mapped["User"] = relationship(
        "User",
        back_populates="item",  # Back reference
        lazy="selectin" # Load user with item
    )
