from aiogram.fsm.state import State, StatesGroup


class AppointmentSG(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_service = State()
    waiting_for_date = State()
    waiting_for_confirmation = State()