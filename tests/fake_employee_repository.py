
from models.employee import Employee


class FakeEmployeeRepository:
    def __init__(self, employees=None):
        self._employees = {
            employee.id: employee
            for employee in (employees or [])
        }

    async def get_all_employees(self):
        return list(self._employees.values())

    async def get_employee_by_id(self, employee_id: int):
        return self._employees.get(employee_id)

    async def add_employee(self, employee: Employee):
        if employee.id is None:
            employee.id = max(self._employees.keys(), default=0) + 1

        self._employees[employee.id] = employee
        return employee

    async def update_employee(
        self,
        employee_id: int,
        updated_employee: Employee,
    ):
        employee = self._employees.get(employee_id)

        if employee:
            employee.name = updated_employee.name
            employee.email = updated_employee.email
            employee.designation = updated_employee.designation
            employee.salary = updated_employee.salary

        return employee

    async def delete_employee(self, employee_id: int):
        return self._employees.pop(employee_id, None)
