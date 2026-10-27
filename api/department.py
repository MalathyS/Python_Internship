from fastapi import APIRouter, Depends


from dependencies import get_department_service

from services.department_service import DepartmentService
from schemas.department import DepartmentCreate, DepartmentResponse

router = APIRouter(prefix="/departments", tags=["Departments"])




@router.post("/", response_model=DepartmentResponse, status_code=201)
async def create_department(
    department: DepartmentCreate,
    service: DepartmentService = Depends(get_department_service),
):
    return await service.create_department(department)

@router.get("/{department_id}", response_model=DepartmentResponse)
async def get_department_by_id(
    department_id: int,
    service: DepartmentService = Depends(get_department_service),
):
    return await service.get_department_by_id(department_id)