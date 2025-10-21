import asyncio
import asyncpg

import os
from dotenv import load_dotenv
from config import settings

# Load environment variables from .env file
load_dotenv()

async def test_postgres_connection():
    """
    Test PostgreSQL database connection and ensure database exists.
    
    This function:
    1. Attempts to connect to PostgreSQL server
    2. Checks if the target database exists
    3. Creates the database if it doesn't exist
    4. Tests connection to the target database
    
    :return: Boolean indicating connection success
    :raises Exception: If connection fails or database operations error
    """
    
    try:        
        db_host = settings.DB_HOST
        db_port = settings.DB_PORT
        db_name = settings.DB_NAME
        db_user = settings.DB_USER
        db_password = settings.DB_PASSWORD
        
        print(f"Try connect to: {db_user}@{db_host}:{db_port}/{db_name}")
        
        # Try to connect to default postgres DB
        conn = await asyncpg.connect(
            host=db_host,
            port=db_port,
            database='postgres',  
            user=db_user,
            password=db_password
        )
        
        version = await conn.fetchval('SELECT version()')
        print(f"Successfully connected to PostgreSQL: {version.split(',')[0]}")
        
        # Is DB already exist?
        db_exists = await conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = $1", db_name
        )
        
        if db_exists:
            print(f"DB '{db_name}' exist")
            await conn.close()
            
            # Connecting to database
            conn = await asyncpg.connect(
                host=db_host,
                port=db_port,
                database=db_name,
                user=db_user,
                password=db_password
            )
            print(f"Successfully connected to '{db_name}'")
            
        else:
            print(f"DB '{db_name}' doesent exist, creating...")
            await conn.execute(f'CREATE DATABASE {db_name}')
            print(f"DB '{db_name}' Created!")
        
        await conn.close()
        return True
        
    except Exception as e:
        print(f"Connection Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing connection to PostgreSQL...")
    result = asyncio.run(test_postgres_connection())
    if result:
        print("Test passed! PostgresQL ready to use")
    else:
        print("Test failed. Check your config")