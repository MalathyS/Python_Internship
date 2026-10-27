
import pytest
import pytest_asyncio

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy.pool import StaticPool

from models.employee import Employee
from models.department import Department
from repositories.employee_repository import EmployeeRepository
from models.base import Base


@pytest_asyncio.fixture
async def repository():
    engine = create_async_engine(
        "sqlite+aiosqlite://",
        poolclass=StaticPool,
    )

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with session_factory() as session:
        yield EmployeeRepository(session)

    await engine.dispose()


@pytest.mark.asyncio
async def test_add_employee(repository):
    employee = Employee(
        name="John Doe",
        email="john.doe@example.com",
        designation="Software Engineer",
        salary=60000.0,
    )

    result = await repository.add_employee(employee)

    assert result.id is not None
    assert result.name == "John Doe"


@pytest.mark.asyncio
async def test_get_employee_by_id(repository):
    employee = Employee(
        name="Jane Smith",
        email="jane@example.com",
        designation="Data Scientist",
        salary=75000.0,
    )

    await repository.add_employee(employee)

    result = await repository.get_employee_by_id(employee.id)

    assert result is not None
    assert result.name == "Jane Smith"


@pytest.mark.asyncio
async def test_get_employee_by_id_returns_none_when_missing(repository):
    result = await repository.get_employee_by_id(999)

    assert result is None


@pytest.mark.asyncio
async def test_get_all_employees(repository):
    await repository.add_employee(
        Employee(
            name="John Doe",
            email="john@example.com",
            designation="Developer",
            salary=60000.0,
        )
    )

    await repository.add_employee(
        Employee(
            name="Jane Smith",
            email="jane@example.com",
            designation="Tester",
            salary=50000.0,
        )
    )

    result = await repository.get_all_employees()

    assert len(result) == 2


@pytest.mark.asyncio
async def test_update_employee(repository):
    employee = Employee(
        name="John Doe",
        email="john.doe@example.com",
        designation="Software Engineer",
        salary=60000.0,
    )

    await repository.add_employee(employee)

    updated_employee = Employee(
        name="John Doe Updated",
        email="john.doe.updated@example.com",
        designation="Senior Software Engineer",
        salary=65000.0,
    )

    result = await repository.update_employee(
        employee.id,
        updated_employee,
    )

    assert result is not None
    assert result.name == "John Doe Updated"


@pytest.mark.asyncio
async def test_update_employee_returns_none_when_missing(repository):
    updated_employee = Employee(
        name="Non-existent Employee",
        email="nonexistent@gmail.com",
        designation="Manager",
        salary=70000.0,
    )

    result = await repository.update_employee(999, updated_employee)

    assert result is None


@pytest.mark.asyncio
async def test_delete_employee(repository):
    employee = Employee(
        name="John Doe",
        email="john.doe@gmail.com",
        designation="Software Engineer",
        salary=60000.0,
    )

    await repository.add_employee(employee)

    result = await repository.delete_employee(employee.id)

    assert result is not None
    assert result.name == "John Doe"


@pytest.mark.asyncio
async def test_delete_employee_returns_none_when_missing(repository):
    result = await repository.delete_employee(999)

    assert result is None
