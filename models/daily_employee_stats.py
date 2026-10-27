from datetime import date, datetime

from sqlalchemy import Date, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class DailyEmployeeStats(Base):
    __tablename__ = "daily_employee_stats"

    id: Mapped[int] = mapped_column(primary_key=True)

    report_date: Mapped[date] = mapped_column(
        Date,
        unique=True,
        nullable=False,
        index=True,
    )

    employee_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )