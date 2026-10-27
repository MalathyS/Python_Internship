
import os

from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
)

load_dotenv()


def build_url(database_name: str):
    return URL.create(
        "mssql+aioodbc",
        username=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.getenv("DB_SERVER", "localhost"),
        port=int(os.getenv("DB_PORT", "1433")),
        database=database_name,
        query={
            "driver": "ODBC Driver 18 for SQL Server",
            "Encrypt": "yes",
            "TrustServerCertificate": "yes",
        },
    )



master_engine = create_async_engine(build_url("master"))


engine = create_async_engine(
    build_url("PythonEmployeeDb"),
    pool_pre_ping=True,
)


SessionFactory = async_sessionmaker(
    engine,
    expire_on_commit=False,
)



async def initialize_database():
   
    async with master_engine.connect() as connection:
       
        connection = await connection.execution_options(
            isolation_level="AUTOCOMMIT"
        )

       
        await connection.execute(
            text("""
                IF DB_ID(N'PythonEmployeeDb') IS NULL
                    CREATE DATABASE PythonEmployeeDb
            """)
        )

    print("Database setup completed.")

   
    from models.employee import Base


    """ async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all) """
       
    print("Employee table created successfully.")

    
    await master_engine.dispose()
