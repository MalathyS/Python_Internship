from pydantic import BaseModel, Field, EmailStr

from schemas.department import DepartmentResponse

class employeeCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    designation: str = Field(..., max_length=100)
    salary: float = Field(..., gt=0)
    department_id: int | None = Field(default=None, ge=1)


class employeeResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    designation: str
    salary: float
    department_id: int | None
    department : DepartmentResponse | None = None

    model_config = {"from_attributes": True}