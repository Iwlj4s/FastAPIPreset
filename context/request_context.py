from fastapi import Depends
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession
from database import models, schema, response_schemas
from database.database import get_db
from repository.user_repository import get_current_user

# TODO: Think about how to improve that
# TODO: Add info about that in README

"""
Request Context Pattern Implementation

This module implements the Request Context pattern, which provides
a convenient way to pass common dependencies between application layers.

Advantages of using Request Context:
1. Simplifies function signatures - fewer parameters
2. Centralized dependency management
3. Easy to add new dependencies (logger, cache, config, etc.)
4. Improves testability - easy to mock context

Alternative: You can use the standard FastAPI approach with separate
dependencies in each endpoint (see README section).
"""

@dataclass
class RequestContext:
    """
    Container for dependencies shared across the entire request.
    
    Attributes:
        db (AsyncSession): Async database session
        current_user (schema.User): Current authenticated user
    
    Future extensibility - easily add:
        - logger: logging.Logger
        - cache: RedisClient  
        - config: AppConfig
        - request_id: str
    """
    db: AsyncSession
    current_user: any

async def get_request_context(db: AsyncSession = Depends(get_db),
                              current_user: any = Depends(get_current_user)) -> RequestContext:
    """
    Dependency function that creates the request context.
    
    This function is automatically called by FastAPI for each request
    and provides a ready-to-use context with all dependencies.
    
    Args:
        db: Database session (automatically injected)
        current_user: Current user (automatically injected)
    
    Returns:
        RequestContext: Context with initialized dependencies
    """
    return RequestContext(db=db, current_user=current_user)