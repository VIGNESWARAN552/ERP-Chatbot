from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv
load_dotenv()
import sys
import os

# Ensure your app directory is in the path to import your modules
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import your SQLAlchemy Base and models
from app.database import Base
from app.models import *  # Import all your models to register them with Base

# Alembic Config object, provides access to .ini file values
config = context.config

# Set up Python logging from config file if present
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# This is the metadata Alembic will use to generate migrations
target_metadata = Base.metadata


def run_migrations_offline():
    url = config.get_main_option("DATABASE_URL")
    if not url:
        raise ValueError("DATABASE_URL is not set in the Alembic config file.")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
