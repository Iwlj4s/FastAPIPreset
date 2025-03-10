import os
from dotenv import load_dotenv

from pathlib import Path

env_path = Path('.') / '.env'  # Getting env path
load_dotenv(dotenv_path=env_path)  # Load env


class Settings:
    """
    Get important data from env file
    """
    DATABASE_URL: str = os.getenv('DB_LITE')
    DATABASE_URL_FOR_ALEMBIC: str = os.getenv('DB_FOR_ALEMBIC')
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    ALGORITHM: str = os.getenv('ALGORITHM')


settings = Settings()  # Create object for easy import and use them


def get_auth_data():
    return {"secret_key": settings.SECRET_KEY, "algorithm": settings.ALGORITHM}
