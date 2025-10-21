import os
from dotenv import load_dotenv

from pathlib import Path

# Load environment variables from .env file
env_path = Path('.') / '.env'  # Getting env path
load_dotenv(dotenv_path=env_path)  # Load env


class Settings:
    """
    Application settings management class.
    All configuration parameters are loaded from environment variables.
    
    To generate SECRET_KEY use:
    node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
    """

    # SQLITE #
    DATABASE_URL: str = os.getenv('DB_LITE')     # Async URL for SQLite
    DATABASE_URL_FOR_ALEMBIC: str = os.getenv('DB_LITE_FOR_ALEMBIC')    # Sync URL for migrations

    # PostgreSQL #
    DB_HOST: str = os.getenv('DB_HOST')
    DB_PORT: str = os.getenv('DB_PORT')
    DB_NAME: str = os.getenv('DB_NAME')
    DB_USER: str = os.getenv('DB_USER')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD')
    DATABASE_URL_POSTGRE: str = os.getenv('DATABASE_URL_POSTGRE')   # Async URL for PostgreSQL
    DATABASE_URL_FOR_ALEMBIC_POSTGRE: str = os.getenv('DATABASE_URL_ALEMBIC_POSTGRE')   # Sync URL for migrations

    # JWT authentication settings

    SECRET_KEY: str = os.getenv('SECRET_KEY')   # Secret key for JWT token signing
    ALGORITHM: str = os.getenv('ALGORITHM')   # Encryption algorithm (HS256)

# Create settings instance for import in other modules
settings = Settings()  


def get_auth_data():
    """
    Returns data for JWT authentication.
    Used in token helper functions.
    """
    return {"secret_key": settings.SECRET_KEY, 
            "algorithm": settings.ALGORITHM}
