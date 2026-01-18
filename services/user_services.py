from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from database import response_schemas

class UserService:
    """
    Service layer for user-related business logic and response formatting.
    Contains operations that transform database models into API response schemas.
    """

    @staticmethod
    async def get_formated_users(users: List) -> response_schemas.UserResponse:
        """
        Transform list of SQLAlchemy User models into API response format.
        
        :param users: List[models.User] - List of User database models

        :return: List[response_schemas.UserResponse] - Formatted users ready for API response

        Note:
            Uses Pydantic schemas to avoid recursion and control response structure.
            Handles serialization and filtering of sensitive data.
        """

        users_list = []
        for user in users:
            user_data = response_schemas.UserResponse(
                id=user.id,
                name=user.name,
                email=user.email,
                bio=user.bio,
            )
            users_list.append(user_data)

        return users_list
    