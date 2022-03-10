from aiogram.types import Message


class AddAdmin():
    def __init__(self, bot, db) -> None:
        self.bot = bot
        self.db = db

    async def __is_admin(self, id, channel: int):
        administrators = await self.bot.get_chat_administrators(channel)
        for admin in administrators:
            if id == admin["user"]["id"] and admin["can_post_messages"] == True:
                return True
        return False

    async def __confirm_admin(self, message: Message):
        channel_id = message.forward_from_chat.id
        user_id = message.from_user.id
        if await self.__is_admin(user_id, channel_id) and await self.__is_admin(self.bot.id, channel_id):
            return True
        else:
            return False

    async def set_admin(self, message: Message) -> str:
        if not await self.__confirm_admin(message):
            return "Вы не админ/ Бот не админ этого канала"
        self.db.set_admin(message.from_user.id)
        self.db.add_channel(message.from_user.id,
                            message.forward_from_chat.id)

        return f"Вы успешно стали администратором канала {message.forward_from_chat.id}"

    async def get_is_admin(self, id, channel):
        return await self.__is_admin(id, channel)
