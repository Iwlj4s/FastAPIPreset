from fastapi import HTTPException
from starlette import status

"""
Helper functions module for HTTP error handling.
Simplifies condition checking and returning standardized errors.
"""


async def CheckHTTP404NotFound(founding_item, text: str):
    """
    Checks if element is found.
    If element is not found (None), throws HTTP 404 error.
    
    :param founding_item: Element to check (can be None)
    :param text: Error text to return
    :return: Original element if found
    :raises HTTPException: 404 if element not found
    """
    if not founding_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=text)

    return founding_item

async def CheckHTTP403FORBIDDEN_BOOL(condition: bool, text: str):
    """
    Checks boolean condition for access permissions.
    If condition is True, throws HTTP 403 error.
    
    :param condition: Boolean condition to check
    :param text: Error text to return
    :raises HTTPException: 403 if condition is True
    """
    if condition:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=text)


async def CheckHTTP401Unauthorized(founding_item, text: str):
    """
    Checks user authorization.
    If element is not found, throws HTTP 401 error.
    
    :param founding_item: Element to check authorization
    :param text: Error text to return
    :return: Original element if authorization successful
    :raises HTTPException: 401 if authorization failed
    """
    if not founding_item:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=text)

    return founding_item


async def CheckHTTP409Conflict(founding_item, text: str):
    """
    Checks for data conflict (duplication).
    If element is found, throws HTTP 409 error.
    
    :param founding_item: Element to check for conflict
    :param text: Error text to return
    :return: Original element if no conflict
    :raises HTTPException: 409 if conflict detected
    """
    if founding_item:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=text)

    return founding_item

async def CheckHTTP400BadRequest(condition: bool, text: str):
    """
    Check for bad request data.
    If condition is True, throws HTTP 400 error.
    
    :param condition: Boolean condition to check
    :param text: Error text to return
    :raises HTTPException: 400 if bad request detected
    """
    if condition:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=text)