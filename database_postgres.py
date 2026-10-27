
import os

from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

load_dotenv()


def build_url(database_name: str):
    return URL.create(
        "postgresql+asyncpg",
        username=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=int(os.getenv("POSTGRES_PORT", "5433")),
        database=database_name,
    )


# NEW: Create the engine for the application database.
engine = create_async_engine(
    build_url(os.environ["POSTGRES_DB"]),
    pool_pre_ping=True,
)

# NEW: Use the same async session pattern as SQL Server.
SessionFactory = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


async def initialize_database():
    database_name = os.environ["POSTGRES_DB"]

    # Connect to the default maintenance database.
    master_engine = create_async_engine(build_url("postgres"))

    try:
        async with master_engine.connect() as connection:
            # CHANGED: PostgreSQL CREATE DATABASE doesn't support
            # "IF NOT EXISTS". Check first, using a parameterized query.
            result = await connection.execute(
                text(
                    "SELECT 1 FROM pg_database WHERE datname = :database_name"
                ),
                {"database_name": database_name},
            )

            if result.scalar_one_or_none() is None:
                # Database identifiers cannot be bound as SQL parameters.
                # Quote the identifier safely using the dialect preparer.
                preparer = connection.dialect.identifier_preparer
                quoted_name = preparer.quote_identifier(database_name)

                await connection.execution_options(
                    isolation_level="AUTOCOMMIT"
                )
                await connection.execute(
                    text(f"CREATE DATABASE {quoted_name}")
                )

        print("Database setup completed.")

    finally:
        await master_engine.dispose()

    # NEW: Create tables using an async connection.
    from models.employee import Base
    from models.user import Base as UserBase


    """ async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all) """
        
print("Employee table created successfully.")
