
import os
import sys
import asyncio
from pathlib import Path
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dotenv import load_dotenv

load_dotenv()

from models.employee import Base, Employee
from models.user import User
from models.department import Department
from models.daily_employee_stats import DailyEmployeeStats

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def get_database_url():
    switch = os.getenv("DB_SWITCH", "sqlserver").lower()

    if switch == "sqlserver":
        from database import build_url
        return build_url("PythonEmployeeDb")

    if switch == "postgres":
        from database_postgres import build_url
        return build_url("PythonEmployeeDb")

    raise ValueError(f"Unsupported DB_SWITCH: {switch}")


def run_migrations_offline():
    url = get_database_url()

    context.configure(
        url=url.render_as_string(hide_password=False),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations():
    database_url = get_database_url()

    connectable = async_engine_from_config(
        {
            "sqlalchemy.url": database_url.render_as_string(
                hide_password=False
            )
        },
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    try:
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)
    finally:
        await connectable.dispose()


def run_migrations_online():
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
