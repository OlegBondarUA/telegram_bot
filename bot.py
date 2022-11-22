import requests

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

from decouple import config
from datetime import datetime

open_weather_token = config('WEATHER_KEY')
tg_bot_token = config('TELEGRAM_TOKEN')
storage = MemoryStorage()
bot = Bot(token=tg_bot_token)

dp = Dispatcher(bot, storage=storage)


class WeatherForm(StatesGroup):
    city_for_one_day_weather = State()
    city_for_five_day_weather = State()
    city_for_hourly_weather = State()


@dp.message_handler(commands=['start'])
async def Start_command(message: types.Message):
    kb = [
        [types.KeyboardButton(text='геолокація', request_location=True)]
        ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )

    await message.reply('Привіт! Вибери на скільки днів ти '
                        'хочеш дізнатися погоду', reply_markup=keyboard)


@dp.message_handler(content_types=['location'])
async def location(message):
    if message.location is not None:
        print(message.location['latitude'])
        print(message.location['longitude'])


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
