
import asyncio
from os import getenv
import os

from dotenv import load_dotenv

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

async def main():
    switch = getenv("DB_SWITCH", "sqlserver").lower()

    if switch == "sqlserver":
        from database import initialize_database, engine
    elif switch == "postgres":
        from database_postgres import initialize_database, engine
    else:
        raise ValueError(f"Unsupported database: {switch}")

    try:
        await initialize_database()
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
