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

check_acess = CheckAcess(bot, users_db, start_handle)


@dp.message_handler(commands="help", state=[None, User_state.admin_started, User_state.user_started])
async def haldle_help(message: types.Message):
    with open("source/help.txt", "r") as help:
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
    await check_acess.check_user(message, state)


@dp.message_handler(Text(equals=["Отправка👍", "Пропуск❌"]), state=User_state.admin_started)
async def show_admin_images(message: types.Message, state: FSMContext):
    # Проверка админ ли отправитель / не убрали ли ему админку
    #  ---
    if message.from_user.id in users_db.get_users("admin"):
        pass
    else:
        await start_handle(message, state)
        return
    try:
        if await add_admin.get_is_admin(message.from_user.id, users_db.get_channel(message.from_user.id))\
                and await add_admin.get_is_admin(bot.id, users_db.get_channel(message.from_user.id)):
            pass
        else:
            users_db.del_admin(message.from_user.id)
            await start_handle(message)
    except:
        users_db.del_admin(message.from_user.id)
        await start_handle(message)
    # ---
        users_db.del_admin(message.from_user.id)
        await start_handle(message)
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
async def acess_root(message: types.Message):
    if not root.check_access:
        return

    if "help" in message.text:
        await bot.send_message(message.chat.id, root.show_help())

    elif "unban_user" in message.text:
        await bot.send_message(message.chat.id, root.unban_user(message))

    elif "ban_user" in message.text:
        await bot.send_message(
            message.chat.id, root.ban_user(message))

    elif "get_list" in message.text:
        await bot.send_message(message.chat.id, root.get_list(message))

    elif "set_admin" in message.text:
        await bot.send_message(message.chat.id, root.set_admin(message))
    elif "del_admin" in message.text:
        await bot.send_message(message.chat.id, root.del_admin(message))


if __name__ == '__main__':
    executor.start_polling(dp)
