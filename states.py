from aiogram.fsm.state import StatesGroup, State


class RegisterState(StatesGroup):
    user_id = State()
    username = State()
    class_number = State()
    class_identifier = State()
