from fastapi import HTTPException

from repositories.department_repository import DepartmentRepository
from models.department import Department
from schemas.department import DepartmentCreate
from schemas.department import DepartmentCreate


class DepartmentService:
    def __init__(self, department_repository: DepartmentRepository):
        self.department_repository = department_repository

    async def get_department_by_name(self, name: str) -> Department | None:
        return await self.department_repository.get_by_name(name)

    async def get_department_by_id(self, department_id: int) -> Department | None:
        return await self.department_repository.get_by_id(department_id)

    async def create_department(self, department: DepartmentCreate):
        name = department.name

        existing_department = await self.department_repository.get_by_name(name)

        if existing_department:
            raise HTTPException(
                status_code=409,
                detail="Department already exists"
            )

        return await self.department_repository.create(name)