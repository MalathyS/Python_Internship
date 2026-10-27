

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from enums.user_role import UserRole
from models.employee import Base as EmployeeBase    


class User(EmployeeBase):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column( String(100),unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    role: Mapped[UserRole] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=0)

 
    