from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_services_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="Women's Haircut — $35", callback_data="service:Womens Haircut")],
        [InlineKeyboardButton(text="Men's Haircut — $25", callback_data="service:Mens Haircut")],
        [InlineKeyboardButton(text="Hair Coloring — $60", callback_data="service:Hair Coloring")],
        [InlineKeyboardButton(text="Manicure — $30", callback_data="service:Manicure")],
        [InlineKeyboardButton(text="❌ Cancel Booking", callback_data="cancel_booking")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_confirmation_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="✅ Confirm", callback_data="confirm_booking"),
            InlineKeyboardButton(text="❌ Cancel", callback_data="cancel_booking")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)