
import pytest
import pytest_asyncio

from models.employee import Employee
from schemas.employee import employeeCreate
from services.employee_service import EmployeeService
from tests.fake_employee_repository import FakeEmployeeRepository


@pytest.fixture
def fake_employee_repository():
    employees = [
        Employee(
            id=1,
            name="John Doe",
            email="john.doe@example.com",
            designation="Software Engineer",
            salary=60000.0,
        ),
        Employee(
            id=2,
            name="Jane Smith",
            email="jane.smith@example.com",
            designation="Data Scientist",
            salary=75000.0,
        ),
    ]
    return FakeEmployeeRepository(employees)


@pytest.fixture
def employee_service(fake_employee_repository):
    return EmployeeService(fake_employee_repository)


@pytest.mark.asyncio
async def test_get_employees(employee_service):
    employees = await employee_service.get_employees()

    assert len(employees) == 2
    assert employees[0].name == "John Doe"
    assert employees[1].name == "Jane Smith"


@pytest.mark.asyncio
async def test_get_employee_by_id(employee_service):
    employee = await employee_service.get_employee_by_id(1)

    assert employee is not None
    assert employee.name == "John Doe"


@pytest.mark.asyncio
async def test_get_employee_by_id_not_found(employee_service):
    employee = await employee_service.get_employee_by_id(999)

    assert employee is None


@pytest.mark.asyncio
async def test_add_employee(employee_service):
    new_employee = employeeCreate(
        name="Alice Johnson",
        email="alice.johnson@example.com",
        designation="Product Manager",
        salary=80000.0,
    )

    result = await employee_service.add_employee(new_employee)

    assert result.id is not None
    assert result.name == "Alice Johnson"


@pytest.mark.asyncio
async def test_update_employee(employee_service):
    updated_employee = employeeCreate(
        name="John Doe Updated",
        email="john.doe.updated@example.com",
        designation="Senior Software Engineer",
        salary=65000.0,
    )

    result = await employee_service.update_employee(1, updated_employee)

    assert result is not None
    assert result.name == "John Doe Updated"


@pytest.mark.asyncio
async def test_update_employee_not_found(employee_service):
    updated_employee = employeeCreate(
        name="Non-existent Employee",
        email="non.existent@example.com",
        designation="Manager",
        salary=70000.0,
    )

    result = await employee_service.update_employee(999, updated_employee)

    assert result is None


@pytest.mark.asyncio
async def test_delete_employee(employee_service):
    result = await employee_service.delete_employee(1)

    assert result is not None
    assert result.name == "John Doe"
