from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboards.reply import get_main_keyboard
from app.services.user_service import UserService

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession, state: FSMContext):
    await state.clear()

    if message.from_user:
        user_service = UserService(session)
        await user_service.get_or_create_user(
            telegram_id=message.from_user.id,
            full_name=message.from_user.full_name,
            username=message.from_user.username
        )

    first_name = message.from_user.first_name if message.from_user else "Guest"
    await message.answer(
        f"Hello, {first_name}! 👋\n\n"
        f"Welcome to **GT Beauty** — a showcase appointment bot powered by **GT Labs**.\n"
        f"Please select an option from the menu below:",
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown"
    )


@router.message(F.text == "🏢 About Us")
async def about_company(message: Message):
    await message.answer(
        "✨ **GT Beauty** is a flagship premium beauty studio.\n\n"
        "We combine world-class beauty services, professional stylists, and high-tech customer management.",
        parse_mode="Markdown"
    )


@router.message(F.text.in_({"💰 Pricing", "✂️ Services"}))
async def show_prices(message: Message):
    await message.answer(
        "✂️ **Our Services & Pricing:**\n\n"
        "• Women's Haircut: $35\n"
        "• Men's Haircut: $25\n"
        "• Hair Coloring: $60\n"
        "• Manicure: $30\n\n"
        "To book a slot, click **📅 Book Appointment** below.",
        parse_mode="Markdown"
    )


@router.message(F.text == "📞 Contacts")
async def show_contacts(message: Message):
    await message.answer(
        "📍 **GT Beauty Contacts:**\n\n"
        "🏠 Address: 42 Innovation Ave, Tech City\n"
        "📞 Phone: +1 (800) 555-0199\n"
        "⏰ Hours: Mon-Sun 10:00 AM - 10:00 PM\n"
        "💬 Support: @gt_labs_support",
        parse_mode="Markdown"
    )