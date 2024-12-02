from typing import List
from sqlalchemy import String, Text, text, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.database import Base


class Something(Base):
    __tablename__ = 'something'
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, index=True, unique=True)
