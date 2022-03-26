from config.config import *
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from logger.logger import *
from states.states import *
from getters_photo.danbooru import get_image_url
from Keyboard.keyboard import create_admin_keyboard, create_user_keyboard
from db_manager.UsersDB import UsersDB
from aiogram.dispatcher.filters import Text, HashTag, ForwardedMessageFilter
from RootUserTools.RootUser import RootUser
from AddAdmin import AddAdmin
from CheckAcess.CheckAcess import CheckAcess

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
users_db = UsersDB("db/users.db")
root = RootUser(ROOT_ACESS, users_db)
add_admin = AddAdmin(bot, users_db)
check_acess = CheckAcess(bot, users_db, add_admin)


@dp.message_handler(commands="start", state=[None, User_state.admin_started, User_state.user_started])
async def start_handle(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id in users_db.get_users("banned"):
        await bot.send_message(message.chat.id, "Вы заблокированы!")
    elif user_id in users_db.get_users("user"):
        await state.update_data(photo_url=get_image_url())
        data = await state.get_data()
        await bot.send_photo(message.chat.id, photo=data["photo_url"], reply_markup=create_user_keyboard())
        await User_state.user_started.set()
    elif user_id in users_db.get_users("admin"):
        await state.update_data(photo_url=get_image_url())
        data = await state.get_data()
        await bot.send_photo(message.chat.id, photo=data["photo_url"], reply_markup=create_admin_keyboard())
        await User_state.admin_started.set()
    elif user_id in users_db.get_users("root"):
        pass
    else:
        await bot.send_message(message.chat.id, users_db.add_user(user_id, message.from_user.full_name))
        await start_handle(message, state)


@dp.message_handler(commands="help", state=[None, User_state.admin_started, User_state.user_started])
async def haldle_help(message: types.Message):
    with open("source/help.txt", "r", encoding="utf-8") as help:
        await bot.send_message(message.chat.id, help.read())


@dp.message_handler(content_types=["text", "photo"], is_forwarded=True,
                    state=[None, User_state.admin_started, User_state.user_started])
async def add_admin_hendler(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, text=await add_admin.set_admin(message))


@dp.message_handler(content_types="text", state=None)
async def handle_nonreg(message: types.Message, state: FSMContext):
    await start_handle(message, state)


@dp.message_handler(Text(equals="Далее🖼"), state=User_state.user_started)
async def show_user_images(message: types.Message, state: FSMContext):
    if not await check_acess.check_user(message, state):
        await start_handle(message, state)


@dp.message_handler(Text(equals=["Отправка👍", "Пропуск❌"]), state=User_state.admin_started)
async def show_admin_images(message: types.Message, state: FSMContext):
    if not await check_acess.check_admin(message):
        await state.reset_state(with_data=True)
        await start_handle(message)
        return
    data = await state.get_data()
    if message.text == "Отправка👍":
        await bot.send_photo(users_db.get_channel(message.from_user.id), data["photo_url"])
        await bot.send_message(message.chat.id, "Отправлено!")
    elif message.text == "Пропуск❌":
        await bot.send_message(message.chat.id, "Пропущено!")
    await state.update_data(photo_url=get_image_url())
    data = await state.get_data()
    await bot.send_photo(message.chat.id, data["photo_url"], reply_markup=create_admin_keyboard())


@ dp.message_handler(HashTag, state=[None, User_state.admin_started, User_state.user_started])
async def acess_root(message: types.Message, state: FSMContext):
    if not root.check_access:
        return

    if message.text.startswith("$help"):
        await bot.send_message(message.chat.id, root.show_help())
    elif message.text.startswith("$unban"):
        await bot.send_message(message.chat.id, root.unban_user(message))
    elif message.text.startswith("$ban"):
        await bot.send_message(message.chat.id, root.ban_user(message))
    elif message.text.startswith("$get_list"):
        await bot.send_message(message.chat.id, root.get_list(message))
    elif message.text.startswith("$set_admin"):
        await bot.send_message(message.chat.id, root.set_admin(message))
    elif message.text.startswith("$del_admin"):
        await bot.send_message(message.chat.id, root.del_admin(message))
    elif message.text.startswith("$msg"):
        await state.update_data(users=root.get_list(message))
        await User_state.select_notification_text.set()
        await bot.send_message(message.chat.id, "Введите сообщение для рассылки! ($ <- для отмены)")


@dp.message_handler(content_types="text", state=User_state.select_notification_text)
async def send_notification(message: types.Message, state: FSMContext) -> None:
    if message.text == "$":
        # Что бы в памяти не болтался словарь пользователей, обнуляем data.
        await state.reset_state(with_data=True)
        await bot.send_message(message.chat.id, "Отменено!")
        return
    data = await state.get_data()
    try:
        await bot.send_message(
            message.chat.id, await root.send_notification(
                bot=bot, users=data["users"], text=message.text))
    finally:
        await state.reset_state(with_data=True)


if __name__ == '__main__':
    executor.start_polling(dp)
