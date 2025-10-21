from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from dotenv import load_dotenv

from config import settings

load_dotenv()

"""
Database management module.
Supports both SQLite (for development) and PostgreSQL (for production).
"""

# SQLITE (uncomment to use SQLite)
# SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# PostgreSQL (recommended for production)
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL_POSTGRE

# Create async database engine
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,  # SQL query logging (disable in production)
    future=True,     # Use new SQLAlchemy 2.0 features
    pool_pre_ping=True,  # Check connection before use  
    pool_recycle=300,    # Reconnect every 300 seconds
)

# Create async session factory
SessionLocal = async_sessionmaker(autocommit=False,  # Autocommit disabled for explicit transaction management
                                  autoflush=False,  # Autoflush disabled
                                  bind=engine)  # Bind to created engine

# Base class for all SQLAlchemy models
Base = declarative_base()

async def get_db():
    """
    Dependency for getting database session.
    Used in Depends() to inject session into routes.
    
    Ensures proper session closure after request completion.
    """
    async with SessionLocal() as db:
        try:
            yield db    # Provide session for use
        finally:
            await db.close()    # Always close session
