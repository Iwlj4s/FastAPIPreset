from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from sqlalchemy.ext.asyncio import AsyncSession

from database.database import engine, Base, get_db

from routes.user_router import user_router
from routes.item_router import item_router
from config import settings

app = FastAPI(
    title="FastAPI Preset",
    description="A ready-to-use FastAPI template with super simple authentication and CRUD operations",
)

# Your frontend url
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# Adding middleware, alowing origins and alowing all methods and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Allowed domains 
    allow_credentials=True, # Allow cookie
    allow_methods=["*"], # Allow all http methods
    allow_headers=["*"], # Allow all headers
)

# Middlewate for wprking with sessions
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)


# Creating tables 
async def create_tables():
    """
    Function creating all tables in DB using SQLAlchemy models
    Running when app startup
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# App launch event
@app.on_event("startup")
async def startup_event():
    """
    Creating tables in DB if they NOT already exist
    """
    await create_tables()


# Here you include your routes from /routes
app.include_router(item_router) # Route for working with "items"
app.include_router(user_router) # Route for working with "users"


@app.get("/")
@app.get("/home")
async def home_page(db: AsyncSession = Depends(get_db)):
    """
    API's home page
    Return base info about service
    """
    return {
        "message": "Welcome to FastAPI Preset - A ready-to-use API template",
        "status_code": 200,
        "data": {},
        "docs_url": "/docs"    # Swagger docs linc
    }

# Start FastAPI: uvicorn main:app --reload