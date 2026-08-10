from aiogram import Router, html
from aiogram.filters import Command, Filter
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from config.config import config
from app.services.appointment_service import AppointmentService


class IsAdminFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user is not None and message.from_user.id == config.ADMIN_ID


router = Router()
router.message.filter(IsAdminFilter())


@router.message(Command("orders"))
async def cmd_orders(message: Message, session: AsyncSession):
    service = AppointmentService(session)
    appointments = await service.get_recent_appointments(limit=10)

    if not appointments:
        await message.answer("📁 No appointments found in database.")
        return

    response_lines = ["📋 <b>Recent Appointments (Last 10):</b>\n"]
    for appt in appointments:
        response_lines.append(
            f"• <b>#{appt.id}</b> | {html.quote(appt.client_name)} (<code>{html.quote(appt.client_phone)}</code>)\n"
            f"  ✂️ {html.quote(appt.service_name)} | 📅 {html.quote(appt.appointment_date)}\n"
            f"  Status: <code>{html.quote(appt.status)}</code>"
        )

    await message.answer("\n\n".join(response_lines), parse_mode="HTML")


@router.message(Command("stats"))
async def cmd_stats(message: Message, session: AsyncSession):
    service = AppointmentService(session)
    stats = await service.get_stats()

    response = (
        "📊 <b>GT Beauty — Analytics & Statistics:</b>\n\n"
        f"• <b>Total Bookings:</b> <code>{stats['total']}</code>\n"
        f"• <b>Bookings Today:</b> <code>{stats['today']}</code>\n"
        f"• <b>Last 7 Days:</b> <code>{stats['week']}</code>"
    )
    await message.answer(response, parse_mode="HTML")