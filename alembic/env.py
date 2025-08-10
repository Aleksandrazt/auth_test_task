import asyncio
import os
from logging.config import fileConfig


from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from alembic import context

# Подключаем модели
import sys
from app.models.base import Base
from app.models.user import User
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

config = context.config

fileConfig(config.config_file_name)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set")

target_metadata = Base.metadata


def run_migrations_offline():
    """Выполнение миграций в оффлайн-режиме."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,  # полезно для обнаружения изменений типов колонок
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Выполнение миграций в онлайн-режиме с асинхронным движком."""
    connectable = create_async_engine(DATABASE_URL, poolclass=pool.NullPool)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())