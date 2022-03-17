from itertools import count
from webbrowser import get
from aiogram import Bot
from aiogram.types import Message
import re
from config.config import ROOT_ACESS


class RootUser():
    """Функционал рут пользователя.
    #
    #
    check_acess(message) -- Проверка есть ли id отправителя message в списке root пользователей.
    show_help() -- Отдаёт строку с списком команд root
    ban_user(message) -- Банит пользователя, id которого есть в message.
    unb
    get_list(message) -- Отдаёт словарь пользователей с role из message.
    """

    def __init__(self, root_users: list, db: object) -> None:
        self.root_users = root_users
        self.db = db

    def check_access(self, message: Message) -> bool:
        return message.from_user.id in self.root_users

    def show_help(self) -> str:
        with open("source/root_help.txt", "r", encoding="utf-8") as help:
            return help.read()

    def __parse_id(self, message: Message) -> str:
        return "".join(re.findall("\d", message.text))

    def ban_user(self, message: Message) -> str:
        return self.db.ban_user(self.__parse_id(message))

    def unban_user(self, message: Message) -> str:
        return self.db.unban_user(self.__parse_id(message))

    def get_list(self, message: Message) -> dict:
        users_dict = dict()
        roles = re.findall(r"user|banned|admin", message.text)
        for role in roles:
            users_with_role = self.db.get_users(role)
            for user in users_with_role:
                users_dict[str(
                    user)] = f"{self.db.get_fullname(user)} ({role})"
        return users_dict

    def set_admin(self, message: Message) -> str:
        return self.db.set_admin(self.__parse_id(message))

    def del_admin(self, message: Message) -> str:
        return self.db.del_admin(self.__parse_id(message))

    async def send_notification(self, bot: Bot, users: dict, text: str) -> str:
        counter = 0
        for user in users:
            try:
                await bot.send_message(int(user), text)
                counter += 1
            except:
                pass

        return f"Отправлено в {counter} чатов"
