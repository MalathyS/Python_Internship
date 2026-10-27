from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.department import Department


class DepartmentRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_name(self, name: str) -> Department | None:
        result = await self.db.execute(
            select(Department).where(Department.name == name)
        )
        return result.scalar_one_or_none()

    async def get_by_id(self, department_id: int) -> Department | None:
        result = await self.db.execute(
            select(Department).where(Department.id == department_id)
        )
        return result.scalar_one_or_none()

    async def create(self, name: str) -> Department:
        department = Department(name=name)

        self.db.add(department)
        await self.db.commit()
        await self.db.refresh(department)

        return department