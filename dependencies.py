from os import getenv
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker ,create_async_engine

from database import SessionFactory as sqlserver_session_factory
from database_postgres import SessionFactory as postgres_session_factory
from repositories.department_repository import DepartmentRepository
from repositories.employee_repository import EmployeeRepository
from services.department_service import DepartmentService


async def get_db():
    switch = getenv("DB_SWITCH", "sqlserver").lower()

    if switch == "postgres":
        session_factory = postgres_session_factory
    elif switch == "sqlserver":
        session_factory = sqlserver_session_factory
    else:
        raise ValueError(f"Unsupported database: {switch}")

    async with session_factory() as db:
        yield db

def get_employee_repository(db: AsyncSession = Depends(get_db)):
    return EmployeeRepository(db)

def get_employee_service(employee_repository: EmployeeRepository = Depends(get_employee_repository)):
    from services.employee_service import EmployeeService
    return EmployeeService(employee_repository)


def get_department_service(
    db: AsyncSession = Depends(get_db),
) -> DepartmentService:
    repository = DepartmentRepository(db)
    return DepartmentService(repository)