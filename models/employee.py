
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.department import Department

from models.base import Base


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    designation: Mapped[str] = mapped_column(String(100), nullable=False)
    salary: Mapped[float] = mapped_column(nullable=False, default=0)
    department_id: Mapped[int | None] = mapped_column(
        ForeignKey("departments.id"),
        nullable=True,
    )

    department: Mapped["Department | None"] = relationship(
        back_populates="employees",
    )
    
    