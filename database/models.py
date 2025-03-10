from typing import List
from sqlalchemy import String, Text, text, ForeignKey, DateTime, func, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.database import Base


class Something(Base):
    __tablename__ = 'something'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False, index=True, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="something")


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)

    something = relationship("Something", back_populates="user")