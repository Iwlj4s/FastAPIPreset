from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, List

from starlette import status
from starlette.responses import Response

from DAO.item_dao import ItemDao
from database.database import get_db
from database import models, schema, response_schemas

from helpers import password_helper, user_helper
from helpers import general_helper
from helpers.general_helper import CheckHTTP404NotFound, CheckHTTP409Conflict
from helpers.token_helper import get_token, verify_token

from DAO.general_dao import GeneralDAO
from DAO.user_dao import UserDAO

from helpers import password_helper


"""
User business logic layer.
Handles user authentication, registration, and user-related operations.
"""


async def sign_up(request: schema.User,
                  db: AsyncSession) -> Dict[str, Any]:
    
    """
    Register a new user in the system.
    Validates email and username uniqueness.
    
    :param request: User registration data
    :param db: Database session

    :return: Success response with user data or error
    :raises HTTPException: 409 if email or username already exists
    """
    # Check for existing email
    email = await UserDAO.get_user_email(db=db, user_email=str(request.email))
    # Check for existing username
    name = await UserDAO.get_user_name(db=db, user_name=str(request.name))

    # Return conflict error if email exists
    await CheckHTTP409Conflict(email, "Email already exists")

    # Return conflict error if username exists
    await CheckHTTP409Conflict(name, "This username already exists")

    print(f"   Original password from request: '{request.password}'")
    print(f"   Password length: {len(request.password)}")
    print(f"   Password type: {type(request.password)}")

    # Hash password and create new user
    hash_password = password_helper.hash_password(request.password)
    print(f"   Hashed password: {hash_password}")
    print(f"   Hashed password length: {len(hash_password)}")

    new_user = models.User(name=request.name, 
                           email=request.email, 
                           password=hash_password)
    db.add(new_user)

    await db.commit()
    await db.refresh(new_user)
    print(f"   User created with ID: {new_user.id}")

    return {
        'message': "Register successfully",
        'status_code': 201,
        'status': "success",
        'data': {
            'id': new_user.id,
            'name': new_user.name,
            'email': new_user.email
        }
    }


async def login(request: schema.UserSignIn,
                response: Response,
                db: AsyncSession) -> Dict[str, Any]:
    
    """
    Authenticate user and generate access token.
    
    :param request: User login credentials
    :param response: HTTP response object
    :param db: Database session

    :return: User data with access token or error
    """
    user = await user_helper.take_access_token_for_user(db=db,
                                                        response=response,
                                                        request=request)
    # Return error if authentication failed
    if response.status_code == status.HTTP_403_FORBIDDEN:
        return {
            'message': "Invalid email and/or password",
            'status_code': 403,
            'error': "FORBIDDEN"
        }

    return {
        "user_access_token": user['user_access_token'],
        "email": user['email'],
        "name": user['name'],
        "id": user['id']
    }


async def get_current_user(db: AsyncSession = Depends(get_db),
                           token: str = Depends(get_token)) -> models.User:
    """
    Get current authenticated user from JWT token.
    Used as dependency in protected routes.
    
    :param db: Database session
    :param token: JWT token from request

    :return: User object or error response
    :raises HTTPException: 401 if token invalid or user not found
    """
    user_id = verify_token(token=token)
    print("user_id in get current user: ", user_id)
    if not user_id:
        return {
            'message': "Token not found",
            'status_code': 401,
        }
    user = await GeneralDAO.get_record_by_id(record_id=user_id,
                                             model=models.User, 
                                             db=db)

    return user


async def get_current_user_items(current_user: schema.User, 
                                 db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    """
    Get all items belonging to the current authenticated user.
    
    :param current_user: Authenticated user
    :param db: Database session

    :return: User's items
    :raises HTTPException: 404 if no items found
    """
    items = await ItemDao.get_items_by_user_id(db=db, user_id=current_user.id)
    await CheckHTTP404NotFound(items, "No items found for this user")

    # Use Response Schema to avoid recursion
    items_data = [
        response_schemas.ItemResponse(
            id=item.id,
            name=item.name,
            description=item.description,
            user_id=item.user_id
        )
        for item in items
    ]

    return {
        "user_id": current_user.id,
        "user_name": current_user.name,
        "items": items_data
    }



async def get_current_user_item(item_id: int,
                                current_user: schema.User,
                                db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    """
    Get specific item belonging to the current user.
    
    :param item_id: ID of item to retrieve
    :param current_user: Authenticated user
    :param db: Database session

    :return: User's specific item
    :raises HTTPException: 404 if item not found or doesn't belong to user
    """
    
    item = await ItemDao.get_item_by_user_id(db=db, 
                                             user_id=current_user.id, 
                                             item_id=item_id)
    await CheckHTTP404NotFound(founding_item=item, text="Item not found")

    # Using Response Schema
    item_data = response_schemas.ItemResponse(
        id=item.id,
        name=item.name,
        description=item.description,
        user_id=item.user_id
    )

    return {
        "user_id": current_user.id,
        "user_name": current_user.name,
        "item": item_data
    }


async def get_all_users(db: AsyncSession) -> List[response_schemas.UserWithItemsResponse]:
    """
    Retrieve all users from the system with their items.
    
    :param db: Database session
    :return: List of all users with their items
    :raises HTTPException: 404 if no users found
    """
    users = await GeneralDAO.get_all_records(db=db, model=models.User)
    await general_helper.CheckHTTP404NotFound(founding_item=users, text="Users not found")
    
    # Format response with user items
    # Use Response Schema to avoid recursion
    users_list = []
    for user in users:
        user_data = response_schemas.UserWithItemsResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            items=[
                response_schemas.ItemResponse(
                    id=item.id,
                    name=item.name,
                    description=item.description,
                    user_id=item.user_id
                )
                for item in user.item
            ]
        )
        users_list.append(user_data)
    
    return users_list