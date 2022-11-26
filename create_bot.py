from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from decouple import config


open_weather_token = config('WEATHER_KEY')
tg_bot_token = config('TELEGRAM_TOKEN')
storage = MemoryStorage()
bot = Bot(token=tg_bot_token)

dp = Dispatcher(bot, storage=storage)
