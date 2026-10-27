from typing import Protocol
from models.employee import Employee


class EmployeeRepository(Protocol):
    async def get_all_employees(self) -> list[Employee]:
        ...

    async def get_employee_by_id(self, employee_id: int) -> Employee | None:
        ...

    async def add_employee(self, employee: Employee) -> Employee:
        ...

    async def update_employee(self, employee_id: int, updated_employee: Employee) -> Employee | None:
        ...

    async def delete_employee(self, employee_id: int) -> Employee | None:
        ...