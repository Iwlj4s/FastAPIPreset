from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

import sys
import os

# Add project root to Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import config and models for Alembic
from config import Settings

from database.database import Base
from database.models import User, Item  

settings = Settings()


# Alembic Config object provides access to .ini values
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set database URL for Alembic migrations
# Choose between SQLite or PostgreSQL URLs from settings
db_url_sqlite = str(settings.DATABASE_URL_FOR_ALEMBIC)
db_url_pg = str(settings.DATABASE_URL_FOR_ALEMBIC_POSTGRE)
config.set_main_option("sqlalchemy.url", str(db_url_pg))    # Now using PostgreSQL

# Set target metadata for 'autogenerate' support
# Alembic will compare this with database to generate migrations
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
