from aiogram.dispatcher.filters.state import StatesGroup, State


class User_state(StatesGroup):
    user_started = State()
    admin_started = State()
    select_notification_text = State()
