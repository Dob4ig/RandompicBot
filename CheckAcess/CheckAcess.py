from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from getters_photo.danbooru import get_image_url
from Keyboard.keyboard import create_user_keyboard


class CheckAcess():
    def __init__(self, bot, db, func) -> None:
        self.bot = bot
        self.db = db
        self.func = func

    async def __send_photo(self, message: Message, state: FSMContext, keyboard):
        await state.update_data(photo_url=get_image_url())
        data = await state.get_data()
        await self.bot.send_photo(message.chat.id, photo=data["photo_url"], reply_markup=keyboard)

    async def check_user(self, message: Message, state: FSMContext) -> bool:
        if message.from_user.id in self.db.get_users("user"):
            await self.__send_photo(message, state, create_user_keyboard())
            return True
        else:
            await self.func(message, state)
            return False


"""
 if message.from_user.id in users_db.get_users("user"):
        await state.update_data(photo_url=get_image_url())
        data = await state.get_data()
        await bot.send_photo(message.chat.id, photo=data["photo_url"], reply_markup=create_user_keyboard())
    else:
        await start_handle(message, state)
        return

"""
