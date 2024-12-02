import os
from dotenv import load_dotenv

from pathlib import Path

env_path = Path('.') / '.env'  # Getting env path
load_dotenv(dotenv_path=env_path)  # Load env


class Settings:
    """
    Get important data from env file
    """
    DATABASE_URL = os.getenv('DB_LITE')


settings = Settings()  # Create object for easy import and use them
