from pydantic import BaseModel, Field

from typing import Union


class Something(BaseModel):
    name: Union[str, None] = Field(default=None, min_length=3, title="Имя чего то")


class User(BaseModel):
    name: Union[str, None] = Field(default=None, min_length=3, title="Имя пользователя")
    email: Union[str, None] = Field(default=None, title="Эл.почта пользователя")
    password: Union[str, None] = Field(default=None, min_length=4, title="Пароль пользователя")


class UserSignIn(BaseModel):
    email: Union[str, None] = Field(default=None, title="Эл.почта пользователя")
    password: Union[str, None] = Field(default=None, min_length=4, title="Пароль пользователя")



# Token #
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None
    id: int