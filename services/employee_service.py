
from fastapi import Depends

from dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.employee_contract import EmployeeRepository
from schemas import employee
from schemas.employee import employeeCreate,employeeResponse
from models.employee import Employee
import logging

class EmployeeService:
    def __init__(self, employee_repository):
        self.employee_repository = employee_repository

   
    
    
    async def get_employees(self):
       
                logging.info("Fetching all employees from the repository.")
                employees = await self.employee_repository.get_all_employees()
                return [employeeResponse.model_validate(employee) for employee in employees]
       
    async def get_employee_by_id(self, employee_id: int):
       
            logging.info(f"Fetching employee with ID {employee_id} from the repository.")
            employee = await self.employee_repository.get_employee_by_id(employee_id)
            return employeeResponse.model_validate(employee) if employee else None
        
       

    async def add_employee(self, employee: employeeCreate):
       
            logging.info("Adding new employee to the repository.")
            employee_data = employee.model_dump()
            employee_data = Employee(**employee_data)
            new_employee = await self.employee_repository.add_employee(employee_data)
            return employeeResponse.model_validate(new_employee)
        
        

    async def update_employee(self, employee_id: int, updated_employee: employeeCreate):
       
            logging.info(f"Updating employee with ID {employee_id} in the repository.")
            updated_employee_data = updated_employee.model_dump()
            updated_employee_data = Employee(**updated_employee_data)
            employee = await self.employee_repository.update_employee(employee_id, updated_employee_data)
            return employeeResponse.model_validate(employee) if employee else None
       
    async def delete_employee(self, employee_id: int):
      
            logging.info(f"Deleting employee with ID {employee_id} from the repository.")
            employee = await self.employee_repository.delete_employee(employee_id)
            return employeeResponse.model_validate(employee) if employee else None
       