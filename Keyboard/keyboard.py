from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def create_admin_keyboard(resize_keyboard=True, one_time_keyboard=True) -> ReplyKeyboardMarkup:
    admin_keyboard = ReplyKeyboardMarkup(
        resize_keyboard=resize_keyboard, one_time_keyboard=one_time_keyboard)
    admin_keyboard.add(KeyboardButton("Отправка👍"))
    admin_keyboard.add(KeyboardButton("Пропуск❌"))
    return admin_keyboard


def create_user_keyboard(resize_keyboard=True, one_time_keyboard=True) -> ReplyKeyboardMarkup:
    user_keyboard = ReplyKeyboardMarkup(
        resize_keyboard=resize_keyboard, one_time_keyboard=one_time_keyboard)
    user_keyboard.add(KeyboardButton("Далее🖼"))
    return user_keyboard
