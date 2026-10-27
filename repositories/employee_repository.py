
from unittest import result

from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from exception_handler import DuplicateEmployeeEmailError
from repositories.employee_contract import EmployeeRepository as EmployeeRepositoryContract
from models.employee import Employee
from logging_config import logger as log


class EmployeeRepository(EmployeeRepositoryContract):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all_employees(self):
        log.info("Fetching all employees from the database.")

        result = await self._session.execute(
            select(Employee).options(
                selectinload(Employee.department)
            )
        )

        return result.scalars().all()
    async def get_employee_by_id(self, employee_id: int):
        log.info(
            f"Fetching employee with ID {employee_id} from the database."
        )

        result = await self._session.execute(
            select(Employee)
            .options(selectinload(Employee.department))
            .where(Employee.id == employee_id)
        )

        return result.scalar_one_or_none()

    async def add_employee(self, employee: Employee):
        try:
            log.info("Adding new employee to the database.")

            self._session.add(employee)
            await self._session.commit()

            return await self.get_employee_by_id(employee.id)

        except IntegrityError as exc:
            await self._session.rollback()
            raise DuplicateEmployeeEmailError() from exc

    async def update_employee(
    self,
    employee_id: int,
    updated_employee: Employee):
        try:
            employee = await self.get_employee_by_id(employee_id)

            log.info(f"Updating employee with ID {employee_id}.")

            if not employee:
                return None

            employee.name = updated_employee.name
            employee.email = updated_employee.email
            employee.designation = updated_employee.designation
            employee.salary = updated_employee.salary
            employee.department_id = updated_employee.department_id

            await self._session.commit()

            return await self.get_employee_by_id(employee_id)

        except IntegrityError as exc:
            await self._session.rollback()
            raise DuplicateEmployeeEmailError() from exc
            

    async def delete_employee(self, employee_id: int):
    
            employee = await self.get_employee_by_id(employee_id)
            log.info(f"Deleting employee with ID {employee_id}.")
            if employee:
                await self._session.delete(employee)
                await self._session.commit()
                return employee
   
