from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from database import response_schemas

class ItemService:
    """
    Service layer for item-related business logic and response formatting.
    Transforms database models into API responses with proper serialization.
    """

    @staticmethod
    async def get_formated_items(items: List) -> response_schemas.ItemResponse:
        """
        Transform list of SQLAlchemy Item models into API response format.
        Includes user information to avoid N+1 query problem in API responses.
        
        :param users:  items: List[models.Item] - List of Item database models

        :return:  List[response_schemas.ItemWithUserResponse] - Formatted items with user data
        
        Note:
            Includes user information in response for client convenience.
            Uses joined loading to avoid multiple database queries.
        """

        items_list = []
        for item in items:
            item_data = response_schemas.ItemWithUserResponse(
                id=item.id,
                name=item.name,
                description=item.description,
                user_id=item.user.id,
                user_name=item.user.name,
                user_email=item.user.email
            )
            items_list.append(item_data)

        return items_list
    