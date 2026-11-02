import os
from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import func, update
from sqlalchemy.dialects.postgresql import insert

from database_postgres import SessionFactory
from logging_config import logger as log
from models.daily_employee_stats import DailyEmployeeStats
from models.processed_events import ProcessedEvent


async def process_employee_created_event(
    event_id: str,
    employee_id: int,
) -> bool:
    today = datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).date()

    async with SessionFactory() as session:
        try:
            # 1. Register the event if it hasn't been processed.
            event_statement = (
                insert(ProcessedEvent)
                .values(
                    event_id=event_id,
                    event_type="employee_created",
                )
                .on_conflict_do_nothing(
                    index_elements=["event_id"]
                )
                .returning(ProcessedEvent.event_id)
            )

            result = await session.execute(event_statement)
            inserted_event_id = result.scalar_one_or_none()

            if inserted_event_id is None:
                # This event was already processed.
                await session.rollback()
                log.info(
                    "Duplicate employee event ignored: %s",
                    event_id,
                )
                return False

            # 2. Increment today's count, inserting the row if needed.
            stats_statement = (
                insert(DailyEmployeeStats)
                .values(
                    report_date=today,
                    employee_count=1,
                )
                .on_conflict_do_update(
                    index_elements=["report_date"],
                    set_={
                        "employee_count":
                            DailyEmployeeStats.employee_count + 1,
                        "updated_at": func.now(),
                    },
                )
            )

            await session.execute(stats_statement)

            # 3. Commit the event record and counter together.
            await session.commit()

            log.info(
                "Employee event processed: event_id=%s employee_id=%s",
                event_id,
                employee_id,
            )
            return True

        except Exception:
            await session.rollback()
            log.exception(
                "Failed to process employee event: %s",
                event_id,
            )
            raise