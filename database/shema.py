from pydantic import BaseModel, Field

from typing import Union


class Something(BaseModel):
    name: Union[str, None] = Field(default=None, min_length=3, title="Имя чего то")
    