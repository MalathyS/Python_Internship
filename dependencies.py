import os
from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.department_repository import DepartmentRepository
from repositories.employee_repository import EmployeeRepository
from services.department_service import DepartmentService


def get_session_factory():

    switch = os.getenv("DB_SWITCH", "sqlserver").lower()

    if switch == "sqlserver":
        from database import SessionFactory
        return SessionFactory

    if switch == "postgres":
        from database_postgres import SessionFactory
        return SessionFactory

    if switch == "mysql":
        from database import SessionFactory
        return SessionFactory

    raise ValueError(
        f"Unsupported DB_SWITCH: {switch}. "
        "Supported values: sqlserver, postgres, mysql"
    )


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    session_factory = get_session_factory()

    async with session_factory() as db:
        yield db


def get_employee_repository(
    db: AsyncSession = Depends(get_db),
):
    return EmployeeRepository(db)


def get_employee_service(
    employee_repository: EmployeeRepository = Depends(
        get_employee_repository
    ),
):
    from services.employee_service import EmployeeService
    return EmployeeService(employee_repository)


def get_department_service(
    db: AsyncSession = Depends(get_db),
) -> DepartmentService:
    repository = DepartmentRepository(db)
    return DepartmentService(repository)
