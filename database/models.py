from typing import List
from sqlalchemy import String, ForeignKey, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.database import Base


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String)

    something: Mapped[List["Something"]] = relationship(
        "Something",
        back_populates="user",
        lazy="selectin"
    )


class Something(Base):
    __tablename__ = 'something'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user: Mapped["User"] = relationship(
        "User",
        back_populates="something",
        lazy="selectin"
    )
