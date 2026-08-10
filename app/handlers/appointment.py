import logging
from aiogram import Router, F, html
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramAPIError
from sqlalchemy.ext.asyncio import AsyncSession

from config.config import config
from app.states.appointment import AppointmentSG
from app.keyboards.reply import get_cancel_keyboard, get_phone_keyboard, get_main_keyboard
from app.keyboards.inline import get_services_keyboard, get_confirmation_keyboard
from app.utils.validators import validate_phone
from app.services.appointment_service import AppointmentService

logger = logging.getLogger(__name__)
router = Router()


@router.message(F.text == "📅 Book Appointment")
async def start_booking(message: Message, state: FSMContext):
    await state.set_state(AppointmentSG.waiting_for_name)
    await message.answer(
        "Let's book your appointment! 📝\n\n"
        "Please enter your full name:",
        reply_markup=get_cancel_keyboard()
    )


@router.message(AppointmentSG.waiting_for_name, F.text)
async def process_name(message: Message, state: FSMContext):
    if not message.text or len(message.text.strip()) < 2:
        await message.answer("Please enter a valid name (at least 2 characters).")
        return

    await state.update_data(client_name=message.text.strip())
    await state.set_state(AppointmentSG.waiting_for_phone)
    await message.answer(
        "Got it! Now please share your phone number using the button below or type it in (e.g. +1234567890):",
        reply_markup=get_phone_keyboard()
    )


@router.message(AppointmentSG.waiting_for_phone, F.contact)
@router.message(AppointmentSG.waiting_for_phone, F.text)
async def process_phone(message: Message, state: FSMContext):
    if message.contact:
        phone = message.contact.phone_number
    else:
        phone = message.text.strip()
        if not validate_phone(phone):
            await message.answer("Invalid phone number format. Please enter a valid number (e.g. +1234567890):")
            return

    await state.update_data(client_phone=phone)
    await state.set_state(AppointmentSG.waiting_for_service)
    await message.answer(
        "Select the service you would like to book:",
        reply_markup=get_services_keyboard()
    )


@router.callback_query(AppointmentSG.waiting_for_service, F.data.startswith("service:"))
async def process_service(callback: CallbackQuery, state: FSMContext):
    service_name = callback.data.split("service:")[1]
    await state.update_data(service_name=service_name)
    await state.set_state(AppointmentSG.waiting_for_date)

    await callback.message.edit_text(
        f"Selected service: <b>{html.quote(service_name)}</b>\n\n"
        f"Please enter your preferred date and time (e.g. Tomorrow at 15:00):",
        parse_mode="HTML"
    )
    await callback.answer()


@router.message(AppointmentSG.waiting_for_date, F.text)
async def process_date(message: Message, state: FSMContext):
    if not message.text or len(message.text.strip()) < 3:
        await message.answer("Please enter a valid date and time.")
        return

    await state.update_data(appointment_date=message.text.strip())
    await state.set_state(AppointmentSG.waiting_for_confirmation)

    data = await state.get_data()
    summary = (
        "📋 <b>Appointment Summary:</b>\n\n"
        f"👤 <b>Name:</b> {html.quote(data['client_name'])}\n"
        f"📞 <b>Phone:</b> {html.quote(data['client_phone'])}\n"
        f"✂️ <b>Service:</b> {html.quote(data['service_name'])}\n"
        f"📅 <b>Date/Time:</b> {html.quote(data['appointment_date'])}\n\n"
        "Is this information correct?"
    )

    await message.answer(summary, reply_markup=get_confirmation_keyboard(), parse_mode="HTML")


@router.callback_query(AppointmentSG.waiting_for_confirmation, F.data == "confirm_booking")
async def confirm_booking(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    user_id = callback.from_user.id

    try:
        appointment_service = AppointmentService(session)
        appointment = await appointment_service.create_appointment(
            user_id=user_id,
            client_name=data["client_name"],
            client_phone=data["client_phone"],
            service_name=data["service_name"],
            appointment_date=data["appointment_date"]
        )
    except Exception:
        await callback.answer("Error saving booking. Please try again.", show_alert=True)
        return

    await state.clear()

    await callback.message.edit_text(
        f"🎉 <b>Booking Confirmed!</b>\n\n"
        f"Thank you, <b>{html.quote(data['client_name'])}</b>. Your booking ID is <code>#{appointment.id}</code>.\n"
        f"Our manager will contact you shortly.",
        parse_mode="HTML"
    )

    admin_notification = (
        f"🚨 <b>NEW BOOKING RECEIVED!</b> (ID: <code>#{appointment.id}</code>)\n\n"
        f"👤 <b>Client:</b> {html.quote(data['client_name'])}\n"
        f"📞 <b>Phone:</b> {html.quote(data['client_phone'])}\n"
        f"✂️ <b>Service:</b> {html.quote(data['service_name'])}\n"
        f"📅 <b>Date:</b> {html.quote(data['appointment_date'])}"
    )

    try:
        await callback.bot.send_message(
            chat_id=config.ADMIN_ID,
            text=admin_notification,
            parse_mode="HTML"
        )
    except TelegramAPIError as e:
        logger.error(f"Failed to send admin notification to {config.ADMIN_ID}: {e}", exc_info=True)

    await callback.answer("Booking complete!")


@router.callback_query(F.data == "cancel_booking")
@router.message(F.text == "❌ Cancel")
async def cancel_booking(event: Message | CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    text = "Booking process cancelled. Returning to main menu."

    if isinstance(event, CallbackQuery):
        await event.message.edit_text(text)
        await event.answer("Cancelled")
    else:
        await event.answer(text, reply_markup=get_main_keyboard())