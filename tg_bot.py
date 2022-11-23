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
        [types.KeyboardButton(text="На 1 день")] +
        [types.KeyboardButton(text="На 5 днів")],
        [types.KeyboardButton(text="Погодинна погода")],
        [types.KeyboardButton(text='Геолокація', request_location=True)]
        ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )

    await message.reply('Привіт! Вибери на скільки днів ти '
                        'хочеш дізнатися погоду', reply_markup=keyboard)


@dp.message_handler(text='На 1 день')
async def weather_1_day(message: types.Message):
    await bot.send_message(message.chat.id, "Чудовий вибір!, Введи назву міста")
    await WeatherForm.city_for_one_day_weather.set()


@dp.message_handler(state=WeatherForm.city_for_one_day_weather)
async def get_weather(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)

    try:
        request = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q='
            f'{message.text}&appid={open_weather_token}&units=metric'
        )
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
            f'Гарного дня!', reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
    except Exception as error:
        print(error)
        await message.reply('\U00002620Перевірте назву міста\U00002620')


@dp.message_handler(text='На 5 днів')
async def weather_5_day(message: types.Message):
    await message.reply("Введи назву міста")
    await WeatherForm.city_for_five_day_weather.set()


@dp.message_handler(state=WeatherForm.city_for_five_day_weather)
async def get_weathers(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)

    try:
        request = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?'
                               f'q={message.text}&appid={open_weather_token}&units=metric')

        data = request.json()

        weather = []
        for item in data['list'][0:34:8]:
            if item['weather'][0]['main'] in code_to_smile:
                wd = code_to_smile[item['weather'][0]['main']]
            else:
                wd = 'Глянь у вікно, не розумію що там за погода!'
            result = (
                f'### {str(datetime.fromtimestamp(item["dt"]))[:10]} ###\n'
                f'Погода в місті: {data["city"]["name"]}\n'
                f'Температура: {float("{:.1f}".format(item["main"]["temp"]))}C°'
                f' {wd}\n'
                f'Вологість: {item["main"]["humidity"]}%\n'
                f'Тиск: {item["main"]["pressure"]} мм.рт.ст\n'
                f'Вітер: {item["wind"]["speed"]} м/с\n'
                f'Видимість: {item["visibility"]}\n\n'
            )
            weather.append(result)
        await message.reply(f'{weather[0]} {weather[1]} {weather[2]} '
                            f'{weather[3]} {weather[4]}'
                            )
        await message.reply('Гарного дня!', reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
    except Exception as error:
        print(error)
        await message.reply('\U00002620Перевірте назву міста\U00002620')


@dp.message_handler(text='Погодинна погода')
async def weather_5_day(message: types.Message):
    await message.reply("Введи назву міста")
    await WeatherForm.city_for_hourly_weather.set()


@dp.message_handler(state=WeatherForm.city_for_hourly_weather)
async def get_weathers(message: types.Message, state: FSMContext):
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
                wd = 'Глянь у вікно, не розумію що там за погода!'
            result = (
                f'### {str(datetime.fromtimestamp(item["dt"]))} ###\n'
                f'Погода в місті: {data["city"]["name"]}\n'
                f'Температура: {float("{:.1f}".format(item["main"]["temp"]))}C°'
                f' {wd}\n'
                f'Вологість: {item["main"]["humidity"]}%\n'
                f'Тиск: {item["main"]["pressure"]} мм.рт.ст\n'
                f'Вітер: {item["wind"]["speed"]} м/с\n'
                f'Видимість: {item["visibility"]}\n\n'
            )
            weather.append(result)
        await message.reply(f'{weather[0]} {weather[1]} {weather[2]} '
                            f'{weather[3]} {weather[4]} {weather[5]} '
                            f'{weather[6]} {weather[7]}'
                            )

        await message.reply('Гарного дня!', reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
    except Exception as error:
        print(error)
        await message.reply('\U00002620Перевірте назву міста\U00002620')


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
