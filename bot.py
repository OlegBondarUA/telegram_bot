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

code_to_smile = {
        'Clear': 'Ясно \U00002600',
        'Clouds': 'Хмарно \U00002601',
        'Overcast clouds': 'Похмурі хмари \U00002601',
        'Rain': 'Дощ \U00002614',
        'Light rain': 'Невеликий дощ \U00002614',
        'Drizzle': 'Дощ \U00002614',
        'Thunderstorm': 'Сніг \U0001F328',
        'Snow': 'Сніг \U0001F328',
        'Light snow': 'Невеликий сніг \U0001F328',
        'Mist': 'Туман \U0001F32B',
        'Light mist': 'Туман \U0001F32B'
    }


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

    await message.reply('Привіт! Обери на скільки днів ти '
                        'хочеш дізнатися погоду', reply_markup=keyboard)


@dp.message_handler(content_types=['location'])
async def location_weather(message):
    try:
        if message.location is not None:
            lat = message.location['latitude']
            lon = message.location['longitude']

            request = requests.get(
                f'https://api.openweathermap.org/data/2.5/weather?'
                f'lat={lat}&lon={lon}&appid={open_weather_token}&units=metric')

            data = request.json()

            city = data['name']
            cur_weather = data['main']['temp']

            weather_description = data['weather'][0]['main']
            if weather_description in code_to_smile:
                wd = code_to_smile[weather_description]
            else:
                wd = 'Глянь у вікно, не розумію що там за погода!'
            humidity = data['main']['humidity']
            pressure = data['main']['pressure']
            wind = data['wind']['speed']
            sunrise_timestamp = \
                datetime.fromtimestamp(data['sys']['sunrise'])
            sunset_timestamp = \
                datetime.fromtimestamp(data['sys']['sunset'])
            length_of_the_day = \
                datetime.fromtimestamp(data['sys']['sunset']) - \
                datetime.fromtimestamp(data['sys']['sunrise'])

            await message.reply(
                f'### {datetime.now().strftime("%Y-%m-%d %H:%M")} ###\n'
                f'Погода в місті: {city}\n'
                f'Температура: {float("{:.1f}".format(cur_weather))}C° {wd}\n'
                f'Вологість: {humidity}%\nТиск: {pressure} мм.рт.ст\n'
                f'Вітер: {wind} м/с\nСхід сонця: {sunrise_timestamp}\n'
                f'Захід сонця: {sunset_timestamp}\n'
                f'Тривалість дня: {length_of_the_day}\n'
                f'Гарного дня!'
            )
    except Exception as error:
        print(error)
        await message.reply('\U00002620Перевірте назву міста\U00002620')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
