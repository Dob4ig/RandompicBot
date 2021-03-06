from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from getters_photo.danbooru import get_image_url
from Keyboard.keyboard import create_user_keyboard


class CheckAcess():
    def __init__(self, bot, db, add_admin) -> None:
        self.bot = bot
        self.db = db
        self.add_admin = add_admin

    async def __send_photo(self, message: Message, state: FSMContext, keyboard):
        await state.update_data(photo_url=get_image_url())
        data = await state.get_data()
        await self.bot.send_photo(message.chat.id, photo=data["photo_url"], reply_markup=keyboard)

    async def check_user(self, message: Message, state: FSMContext) -> bool:
        if message.from_user.id in self.db.get_users("user"):
            await self.__send_photo(message, state, create_user_keyboard())
            return True
        else:
            return False

    async def check_admin(self, message: Message) -> bool:
        try:
            if message.from_user.id in self.db.get_users("admin")\
                    and await self.add_admin.get_is_admin(message.from_user.id, self.db.get_channel(message.from_user.id))\
                    and await self.add_admin.get_is_admin(self.bot.id, self.db.get_channel(message.from_user.id)):
                return True
            else:
                self.db.del_admin(message.from_user.id)
                return False
        except:
            self.db.del_admin(message.from_user.id)
            return False
