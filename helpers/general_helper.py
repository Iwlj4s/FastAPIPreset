from fastapi import HTTPException
from starlette import status

"""
    Here I checking HTTPExceptions
"""


async def CheckHTTP404NotFound(founding_item, text: str):
    if not founding_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=text)

    return founding_item


async def CheckHTTP401Unauthorized(founding_item, text: str):
    if not founding_item:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=text)

    return founding_item


async def CheckHTTP409Conflict(founding_item, text: str):
    if not founding_item:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=text)

    return founding_item
