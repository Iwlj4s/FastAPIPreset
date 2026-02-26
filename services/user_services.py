from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from database import models, response_schemas

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
    
    @staticmethod
    async def create_user_response(user: models.User) -> response_schemas.UserResponse:
        """
        Creating UserResponse from SQLAlchemy User model
        
        :param users: models.User - User database models

        :return: response_schemas.UserResponse - Formatted user ready for API response
        """
        return response_schemas.UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            bio=user.bio or ""
    )
    
    @staticmethod
    async def create_user_with_items_response(user: models.User) -> response_schemas.UserWithItemsResponse:
        """
        Create UserWithItemsResponse from SQLAlchemy User model with related items.

        :param user: models.User - User database model with related items

        :return: response_schemas.UserWithItemsResponse - Formatted user with items for API response
        """
        user_data = await UserService.create_user_response(user=user)
        items = [
             response_schemas.ItemResponse(
                id=item.id,
                name=item.name,
                description=item.description,
                user_id=item.user_id
            )
            for item in user.item
        ]

        return response_schemas.UserWithItemsResponse( 
            **user_data.dict(),  # Transform to dict cause UserWithItemsResponse wait named args for fields 
            items=items
        )
    
    @staticmethod
    async def create_current_user_response(user: models.User, token: str) -> response_schemas.CurrentUserResponse:
        """
        Create CurrentUserResponse from SQLAlchemy User model and JWT token.

        :param user: models.User - User database model
        :param token: str - JWT access token for the authenticated user

        :return: response_schemas.CurrentUserResponse - Formatted current user with access token for API response
        """
        user = await UserService.create_user_response(user=user)

        return response_schemas.CurrentUserResponse(
            **user.dict(),  # Transform to dict cause CurrentUserResponse wait named args for fields
            user_access_token=token
        )

