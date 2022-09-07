import datetime
import requests
import os
from boto.s3.connection import S3Connection
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

weather_token = S3Connection(os.environ['open_weather_token'])
bot_token = S3Connection(os.environ['tg_bot_token'])


def get_weather(city, open_weather_toke):
    code_to_smile = {
        'Clear': 'Ясно \U00002600',
        'Clouds': 'Хмарно \U00002601',
        'Rain': 'Дощ \U00002614',
        'Drizzle': 'Дощ \U00002614',
        'Thunderstorm': 'Сніг \U0001F328',
        'Mist': 'Туман \U0001F32B'
    }

    try:
        r = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={city}'
            f'&appid={open_weather_toke}&units=metric'
        )
        data = r.json()

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
            datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = \
            datetime.datetime.fromtimestamp(data['sys']['sunset'])
        length_of_the_day = \
            datetime.datetime.fromtimestamp(data['sys']['sunset']) - \
            datetime.datetime.fromtimestamp(data['sys']['sunrise'])

        print(f'###{datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}###\n'
              f'Погода в місті: {city}\nТемпература: {cur_weather}C° {wd}\n'
              f'Вологість: {humidity}%\nТиск: {pressure} мм.рт.ст\n'
              f'Вітер: {wind} м/с\nСхід сонця: {sunrise_timestamp}\n'
              f'Захід сонця: {sunset_timestamp}\n'
              f'Тривалість дня: {length_of_the_day}\n'
              f'Гарного дня!')
    except Exception as ex:
        print(ex)
        print('Перевірте назву міста')


sity = input('city?:')
get_weather(sity, weather_token)
bot = Bot(token=bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def Start_command(message: types.Message):
    await message.reply('Привіт! Напиши мені назву міста і я '
                        'тобі пришлю погоду з цього міста')


@dp.message_handler()
async def egt_weather(message: types.Message):
    code_to_smile = {
        'Clear': 'Ясно \U00002600',
        'Clouds': 'Хмарно \U00002601',
        'Rain': 'Дощ \U00002614',
        'Drizzle': 'Дощ \U00002614',
        'Thunderstorm': 'Сніг \U0001F328',
        'Mist': 'Туман \U0001F32B'
    }

    try:
        r = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={message.text}'
            f'&appid={weather_token}&units=metric'
        )
        data = r.json()

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
            datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = \
            datetime.datetime.fromtimestamp(data['sys']['sunset'])
        length_of_the_day = \
            datetime.datetime.fromtimestamp(data['sys']['sunset']) - \
            datetime.datetime.fromtimestamp(data['sys']['sunrise'])

        await message.reply(
            f'###{datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}###\n'
            f'Погода в місті: {city}\nТемпература: {cur_weather}C° {wd}\n'
            f'Вологість: {humidity}%\nТиск: {pressure} мм.рт.ст\n'
            f'Вітер: {wind} м/с\nСхід сонця: {sunrise_timestamp}\n'
            f'Захід сонця: {sunset_timestamp}\n'
            f'Тривалість дня: {length_of_the_day}\n'
            f'Гарного дня!')
    except:
        await message.reply('\U00002620Перевірте назву міста\U00002620')


if __name__ == '__main__':
    executor.start_polling(dp)
