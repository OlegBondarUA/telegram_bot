from pprint import pprint

import requests
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

from decouple import config
from table_for_bot import User, Message


open_weather_token = config('WEATHER_KEY')
tg_bot_token = config('TELEGRAM_TOKEN')
storage = MemoryStorage()
bot = Bot(token=tg_bot_token)

dp = Dispatcher(bot, storage=storage)

code_to_smile = {
        'Clear': 'Clear \U00002600',
        'Clouds': 'Clouds \U00002601',
        'Overcast clouds': 'Overcast clouds \U00002601',
        'Rain': 'Rain \U00002614',
        'Light rain': 'Light rain \U00002614',
        'Drizzle': 'Drizzle \U00002614',
        'Thunderstorm': 'Thunderstorm \U0001F328',
        'Snow': 'Snow \U0001F328',
        'Light snow': 'Light snow \U0001F328',
        'Mist': 'Mist \U0001F32B',
        'Light mist': 'Light mist \U0001F32B'
    }


class WeatherForm(StatesGroup):
    city_for_one_day_weather = State()
    city_for_five_day_weather = State()
    city_for_hourly_weather = State()
    message_client = State()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Hello! I'm a weather bot, I can tell you what the "
                        "weather will be like elsewhere.\nTo start work, "
                        "enter the command /begin")


@dp.message_handler(commands=['begin'])
async def begin_command(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Weather for 1 day")] +
        [types.KeyboardButton(text="Weather for 5 day")] +
        [types.KeyboardButton(text="Hourly weather")],
        [types.KeyboardButton(text="Geolocation weather", request_location=True)],
        [types.KeyboardButton(text="The official weather source")] +
        [types.KeyboardButton(text="Пропозиції для розвитку!")]
        ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )

    await message.reply('Choose your weather option '
                        'and click on the button below.', reply_markup=keyboard)


@dp.message_handler(text='Пропозиції для розвитку!')
async def message_acceptance(message: types.Message):
    await message.reply('Чудово розкажіть нам про помилку у роботі бота'
                        ' або запропонуйте нам щось. Що би ви хотіли '
                        'бачити в цьому боті.')
    await WeatherForm.message_client.set()


@dp.message_handler(state=WeatherForm.message_client)
async def message_save(message: types.Message):

    us = User.get_or_create(
        user_name=str(message['chat']['username']),
        chat_id=int(message['chat']['id'])
    )

    mes = Message.create(
        message=str(message['text']),
        chat_id=int(message['chat']['id'])
    )

    return us, mes


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
