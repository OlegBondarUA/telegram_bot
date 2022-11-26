import requests
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from handlers.smile import code_to_smile

from decouple import config
from datetime import datetime

from handlers import weather_1_day, weather_5_day

open_weather_token = config('WEATHER_KEY')
tg_bot_token = config('TELEGRAM_TOKEN')
storage = MemoryStorage()
bot = Bot(token=tg_bot_token)

dp = Dispatcher(bot, storage=storage)


class WeatherForm(StatesGroup):

    city_for_hourly_weather = State()


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


@dp.message_handler(state='*', commands=['cancel'])
async def cancel_command(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    logging.info('Cancelling state %r', current_state)
    await state.finish()
    await message.answer('We entered the /cancel command',
                         reply_markup=types.ReplyKeyboardRemove())


weather_1_day.register_handlers_weather_1_day(dp)
weather_5_day.register_handlers_weather_5_day(dp)


@dp.message_handler(text='Hourly weather')
async def hourly_weather(message: types.Message):
    await message.reply("Great! Now enter the name of the city or press /cancel"
                        " if you change your mind.")
    await WeatherForm.city_for_hourly_weather.set()


@dp.message_handler(state=WeatherForm.city_for_hourly_weather)
async def get_hourly_weathers(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)

    try:
        request = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?'
                               f'q={message.text}&appid={open_weather_token}&units=metric')

        data = request.json()

        weather = []
        for item in data['list'][0:8:]:
            if item['weather'][0]['main'] in code_to_smile:
                wd = code_to_smile[item['weather'][0]['main']]
            else:
                wd = "Look out the window, " \
                     "I don't understand what kind of weather it is!"

            result = (
                f'### {str(datetime.fromtimestamp(item["dt"]))} ###\n'
                f'Weather in the city: {data["city"]["name"]}\n'
                f'Temperature: {float("{:.1f}".format(item["main"]["temp"]))}C°'
                f' {wd}\n'
                f'Humidity: {item["main"]["humidity"]}%\n'
                f'Pressure: {item["main"]["pressure"]} мм.рт.ст\n'
                f'Wind: {item["wind"]["speed"]} м/с\n'
                f'Visibility: {item["visibility"]}\n\n'
            )
            weather.append(result)
        await message.reply(f'{weather[0]} {weather[1]} {weather[2]} '
                            f'{weather[3]} {weather[4]} {weather[5]} '
                            f'{weather[6]} {weather[7]}'
                            )
        await message.reply('Have a nice day!\n'
                            'To request the weather again, press /begin',
                            reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
    except Exception as error:
        print(error)
        await message.reply(
            "\U00002620Try to check the name of the city\U00002620",
            "If it didn't help, we may have technical problems."
        )


@dp.message_handler(content_types=['location'])
async def get_location_weather(message):
    await message.reply("I'm already forming a message for a second.")
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
                wd = "Look out the window, " \
                     "I don't understand what kind of weather it is!"

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
                f'Weather in the city: {city}\n'
                f'Temperature: {float("{:.1f}".format(cur_weather))}C° {wd}\n'
                f'Humidity: {humidity}%\n'
                f'Pressure: {pressure} мм.рт.ст\n'
                f'Wind: {wind} м/с\n'
                f'Sunrise: {sunrise_timestamp}\n'
                f'Sunset: {sunset_timestamp}\n'
                f'Day length: {length_of_the_day}\n'
                f'Have a nice day!\nTo request the weather again, press /begin',
                reply_markup=types.ReplyKeyboardRemove()
            )
    except Exception as error:
        print(error)
        await message.reply(
            "\U00002620Try to check the name of the city\U00002620",
            "If it didn't help, we may have technical problems."
        )


@dp.message_handler(text='The official weather source')
async def official_source(message):
    await message.answer('https://openweathermap.org/'
                         '\n\nHave a nice day!'
                         '\nTo request the weather again, press /begin\n',
                         reply_markup=types.ReplyKeyboardRemove()
                         )
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
