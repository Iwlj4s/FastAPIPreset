from fastapi import Depends, APIRouter, Response

from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from database.schema import User
from database import schema, models
from helpers import general_helper

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
                  db: AsyncSession = Depends(get_db)):
    """
    Register a new user in the system.
    
    - **request**: User registration data (name, email, password)
    
    Returns created user data with 201 status code.
    """

    return await user_repository.sign_up(request, db)


@user_router.post("/sign_in", status_code=200)
async def sign_in(request: schema.UserSignIn,
                  response: Response,
                  db: AsyncSession = Depends(get_db)):
    """
    Authenticate user and return access token.
    
    - **request**: User login credentials (email, password)
    
    Returns user data with JWT access token in cookie.
    """

    return await user_repository.login(request, response, db)


@user_router.post("/logout")
async def logout(response: Response):
    """
    Logout user by clearing authentication cookie.
    
    Clears the user_access_token cookie from browser.
    """

    response.delete_cookie(key='user_access_token')
    return {'message': 'User logout'}


@user_router.get("/me/", status_code=200)
async def get_me(user_data: User = Depends(get_current_user)):
    """
    Get current authenticated user's profile.
    Requires valid JWT token.
    
    Returns current user's data.
    """

    return user_data


@user_router.get("/user/{user_id}", status_code=200)
async def get_user(user_id: int,
                   db: AsyncSession = Depends(get_db)):
    """
    Get user profile by ID.
    Public endpoint - no authentication required.
    
    - **user_id**: ID of user to retrieve (path parameter)
    
    Returns user data with their items.
    """

    user = await GeneralDAO.get_item_by_id(db=db, item=models.User, item_id=int(user_id))
    await general_helper.CheckHTTP404NotFound(founding_item=user, text="User not found")
    return {
        'user_id:': user.id,
        'user_name:': user.name,
        'user_email': user.email,
        'items': user.item
    }


@user_router.get("/")
async def get_users_for_user(db: AsyncSession = Depends(get_db)):
    """
    Get list of all users in the system.
    Public endpoint - no authentication required.
    
    Returns list of all users with their items.
    """

    users_list = await user_repository.get_all_users(db=db)
    return users_list


@user_router.get("/me/items", status_code=200)
async def get_current_user_items(current_user: schema.User = Depends(get_current_user),
                                 db: AsyncSession = Depends(get_db)):
    """
    Get all items belonging to the current authenticated user.
    Requires valid JWT token.
    
    Returns user's items with ownership information.
    """

    return await user_repository.get_current_user_items(current_user=current_user, db=db)


@user_router.get("/me/item/{item_id}", status_code=200)
async def get_current_user_item(item_id: int,
                                current_user: schema.User = Depends(get_current_user),
                                db: AsyncSession = Depends(get_db)):
    """
    Get specific item belonging to the current user.
    Requires valid JWT token and item ownership.
    
    - **item_id**: ID of item to retrieve (path parameter)
    
    Returns specific item data with user context.
    """

    return await user_repository.get_current_user_item(item_id=item_id,
                                                       current_user=current_user,
                                                       db=db)
