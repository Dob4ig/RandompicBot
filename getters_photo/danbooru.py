from config.config import *
import requests
from random import randint
from logger.logger import *


def get_image_url() -> str:
    page = requests.get(
        f"https://danbooru.donmai.us/posts.json?api_key={DANBOORU_TOKEN}&login={DANBOORU_LOGIN}&page=b999999999&limit=200")
    page_json = page.json()
    logging.info("Бот получил картинку из danbooru")
    return page_json[randint(0, 199)]["large_file_url"]
