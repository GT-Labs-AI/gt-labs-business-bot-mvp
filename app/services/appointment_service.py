import logging
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError

from app.database.models import Appointment

logger = logging.getLogger(__name__)


class AppointmentService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_appointment(
        self,
        user_id: int,
        client_name: str,
        client_phone: str,
        service_name: str,
        appointment_date: str
    ) -> Appointment:
        """Create a new appointment with transaction safety."""
        appointment = Appointment(
            user_id=user_id,
            client_name=client_name,
            client_phone=client_phone,
            service_name=service_name,
            appointment_date=appointment_date,
            status="pending"
        )
        try:
            self.session.add(appointment)
            await self.session.commit()
            await self.session.refresh(appointment)
            return appointment
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Failed to create appointment in DB: {e}", exc_info=True)
            raise

    async def get_recent_appointments(self, limit: int = 10) -> list[Appointment]:
        """Fetch latest appointments."""
        stmt = select(Appointment).order_by(Appointment.id.desc()).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_stats(self) -> dict[str, int]:
        """Calculate stats using naive UTC datetimes compatible with SQLite."""
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        start_of_today = datetime(now.year, now.month, now.day)
        seven_days_ago = now - timedelta(days=7)

        total_stmt = select(func.count(Appointment.id))
        total_res = await self.session.execute(total_stmt)
        total_count = total_res.scalar() or 0

        today_stmt = select(func.count(Appointment.id)).where(Appointment.created_at >= start_of_today)
        today_res = await self.session.execute(today_stmt)
        today_count = today_res.scalar() or 0

        week_stmt = select(func.count(Appointment.id)).where(Appointment.created_at >= seven_days_ago)
        week_res = await self.session.execute(week_stmt)
        week_count = week_res.scalar() or 0

        return {
            "total": total_count,
            "today": today_count,
            "week": week_count,
        }