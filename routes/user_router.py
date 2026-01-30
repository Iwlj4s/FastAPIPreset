from fastapi import Depends, APIRouter, Response
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, List

from DAO.user_dao import UserDAO
from context.request_context import RequestContext, get_request_context
from database.database import get_db
from database import schema, models, response_schemas
from helpers import exception_helper

from repository.user_repository import get_current_user
from repository import user_repository

from DAO.general_dao import GeneralDAO

"""
User API routes.
Defines REST endpoints for user authentication and management.
"""

# Router configuration with prefix and tags for Swagger documentation
user_router = APIRouter(
    prefix="/users",    # All routes will be prefixed with /users/API
    tags=["user_router"]    # Grouped under "Users" in Swagger UI
)


@user_router.post("/sign_up", status_code=201)
async def sign_up(request: schema.User,
                  db: AsyncSession = Depends(get_db)) -> response_schemas.UserCreateResponse:
    """
    Register a new user in the system.
    
    - **request**: User registration data (name, email, password)
    
    Returns created user data with 201 status code.
    """

    return await user_repository.sign_up(request, db)

@user_router.post("/sign_in", status_code=200)
async def sign_in(request: schema.UserSignIn,
                  response: Response,
                  db: AsyncSession = Depends(get_db)) -> response_schemas.UserLoginResponse:
    """
    Authenticate user and return access token.
    
    - **request**: User login credentials (email, password)
    
    Returns user data with JWT access token in cookie.
    """

    return await user_repository.login(request, response, db)

@user_router.post("/logout")
async def logout(response: Response) -> Dict[str, str]:
    """
    Logout user by clearing authentication cookie.
    
    Clears the user_access_token cookie from browser.
    """

    response.delete_cookie(key='user_access_token')
    return {'message': 'User logout'}

@user_router.get("/")
async def get_users_for_user(db: AsyncSession = Depends(get_db)) -> response_schemas.UserListResponse:
    """
    Get list of all users in the system.
    Public endpoint - no authentication required.
    
    Returns list of all users with their items.
    """

    return await user_repository.get_all_users(db=db)

@user_router.get("/user/{user_id}", status_code=200)
async def get_user(user_id: int,
                   db: AsyncSession = Depends(get_db)) -> response_schemas.UserWithItemsDataResponse:
    """
    Get user profile by ID.
    Public endpoint - no authentication required.
    
    - **user_id**: ID of user to retrieve (path parameter)
    
    Returns user data with their items.
    """

    # Use Response Schema to avoid recursion
    user_data = await UserDAO.get_user_with_items(user_id=user_id, db=db)
    
    return response_schemas.UserWithItemsDataResponse(
        message="User retrieved successfully",
        status_code=200,
        data=user_data
    )

@user_router.get("/me/", status_code=200)
async def get_me(user_data: schema.User = Depends(get_current_user)) -> schema.User:
    """
    Get current authenticated user's profile.
    Requires valid JWT token.
    
    Returns current user's data (Current user with items).
    """

    return user_data

@user_router.patch("/me/update", status_code=200)
async def update_me(user_data: schema.UserUpdate, 
                    request_context: RequestContext = Depends(get_request_context)) -> response_schemas.UserUpdateResponse:
    """
    Update current user using PATCH method.
    Requires valid JWT token.

    - **user_data**: Data to update (request body)
    - **request_context**: Request Context which use basic stuff:
        - **current_user**: Automatically injected authenticated user
        - **db**: Database session dependency

    Returns updated current user's data.
    """

    return await user_repository.update_me(user_id=request_context.current_user.id,
                                           user_data=user_data,
                                           current_user=request_context.current_user,
                                           db=request_context.db)

@user_router.get("/me/items", status_code=200)
async def get_current_user_items(request_context: RequestContext = Depends(get_request_context)) -> response_schemas.UserWithItemsDataResponse:
    """
    Get all items belonging to the current authenticated user.
    Requires valid JWT token.

    - **request_context**: Request Context which use basic stuff:
        - **current_user**: Automatically injected authenticated user
        - **db**: Database session dependency
    
    Returns user's items with ownership information.
    """

    return await user_repository.get_current_user_items(current_user=request_context.current_user, db=request_context.db)


@user_router.get("/me/item/{item_id}", status_code=200)
async def get_current_user_item(item_id: int,
                                request_context: RequestContext = Depends(get_request_context)) -> response_schemas.ItemDetailResponse:
    """
    Get specific item belonging to the current user.
    Requires valid JWT token and item ownership.
    
    - **item_id**: ID of item to retrieve (path parameter)
    - **request_context**: Request Context which use basic stuff:
        - **current_user**: Automatically injected authenticated user
        - **db**: Database session dependency
    
    Returns specific item data with user context.
    """

    return await user_repository.get_current_user_item(item_id=item_id,
                                                       current_user=request_context.current_user,
                                                       db=request_context.db)
