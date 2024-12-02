from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from dotenv import load_dotenv

from config import settings

load_dotenv()

SQLALCHEMY_DB_URL = settings.DATABASE_URL

engine = create_async_engine(url=SQLALCHEMY_DB_URL, connect_args={"check_same_thread": False})
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


async def get_db():
    async with SessionLocal() as db:
        try:
            yield db

        finally:
            await db.close()
