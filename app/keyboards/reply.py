from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text="🏢 About Us"), KeyboardButton(text="✂️ Services")],
        [KeyboardButton(text="💰 Pricing"), KeyboardButton(text="📅 Book Appointment")],
        [KeyboardButton(text="📞 Contacts")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder="Select an option from the menu..."
    )


def get_phone_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text="📱 Share Phone Number", request_contact=True)],
        [KeyboardButton(text="❌ Cancel")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )


def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text="❌ Cancel")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)