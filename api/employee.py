from fastapi import APIRouter, Depends, HTTPException


from auth_dependencies import get_current_user, require_role
from dependencies import get_employee_service
from enums.user_role import UserRole
from models.user import User

from repositories.employee_repository import EmployeeRepository
from schemas.employee import employeeCreate, employeeResponse
from services import employee_service
from services.background_tasks import record_employee_creation


router = APIRouter(prefix="/employees", tags=["Employees"])


@router.get("/", response_model=list[employeeResponse])
async def get_employees(employee_service: employee_service = Depends(get_employee_service),
                        current_user: User = Depends(get_current_user)):
    employees =  await employee_service.get_employees()
    return employees

@router.get("/{employee_id}", response_model=employeeResponse)
async def get_employee_by_id(employee_id: int, employee_service: employee_service = Depends(get_employee_service),
                             current_user: User = Depends(get_current_user)):
    employee = await employee_service.get_employee_by_id(employee_id)
    if employee:
        return employee
    else:
        raise HTTPException(status_code=404, detail="Employee not found")

@router.post("/add", response_model=employeeResponse)
async def add_employee(employee: employeeCreate, employee_service: employee_service = Depends(get_employee_service),
                       current_user = Depends(require_role(UserRole.ADMIN))):
    new_employee = await employee_service.add_employee(employee)
    await record_employee_creation()
    return new_employee

@router.put("/update/{employee_id}", response_model=employeeResponse)
async def update_employee(employee_id: int, updated_employee: employeeCreate, employee_service: employee_service = Depends(get_employee_service)):
    employee = await employee_service.update_employee(employee_id, updated_employee)
    if employee:
        return employee
    else:
        raise HTTPException(status_code=404, detail="Employee not found")

@router.delete("/delete/{employee_id}")
async def delete_employee(employee_id: int, employee_service: employee_service = Depends(get_employee_service)):
    employee = await employee_service.delete_employee(employee_id)
    if employee:
        return {"message": "Employee deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Employee not found")