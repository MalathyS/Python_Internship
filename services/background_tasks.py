
import os
from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import func, update
from sqlalchemy.dialects.postgresql import insert as postgres_insert
from sqlalchemy.exc import IntegrityError

from database import SessionFactory as sqlserver_session_factory
from database_postgres import SessionFactory as postgres_session_factory
from models.daily_employee_stats import DailyEmployeeStats
from logging_config import logger as log


async def record_employee_creation():
    switch = os.getenv("DB_SWITCH", "sqlserver").lower()

    if switch == "postgres":
        session_factory = postgres_session_factory
    elif switch == "sqlserver":
        session_factory = sqlserver_session_factory
    else:
        log.error("Unsupported database: %s", switch)
        return

    today = datetime.now(ZoneInfo("Asia/Kolkata")).date()

    async with session_factory() as session:
        try:
            result = await session.execute(
                update(DailyEmployeeStats)
                .where(DailyEmployeeStats.report_date == today)
                .values(
                    employee_count=DailyEmployeeStats.employee_count + 1,
                    updated_at=func.now(),
                )
            )

            if result.rowcount == 0:
                if switch == "postgres":
                    statement = postgres_insert(
                        DailyEmployeeStats
                    ).values(
                        report_date=today,
                        employee_count=1,
                    ).on_conflict_do_update(
                        index_elements=["report_date"],
                        set_={
                            "employee_count":
                                DailyEmployeeStats.employee_count + 1,
                            "updated_at": func.now(),
                        },
                    )
                    await session.execute(statement)

                else:
                    try:
                        session.add(
                            DailyEmployeeStats(
                                report_date=today,
                                employee_count=1,
                            )
                        )
                        await session.flush()
                    except IntegrityError:
                        await session.rollback()

                        # Another request may have inserted today's row.
                        result = await session.execute(
                            update(DailyEmployeeStats)
                            .where(
                                DailyEmployeeStats.report_date == today
                            )
                            .values(
                                employee_count=
                                    DailyEmployeeStats.employee_count + 1,
                                updated_at=func.now(),
                            )
                        )

                        if result.rowcount == 0:
                            raise

            await session.commit()
            log.info(
                "Daily employee creation count updated for %s",
                today,
            )

        except Exception:
            await session.rollback()
            log.exception(
                "Failed to update daily employee creation statistics"
            )
