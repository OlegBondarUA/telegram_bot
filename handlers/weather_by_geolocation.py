import requests

from aiogram import types, Dispatcher

from handlers.smile import code_to_smile
from create_bot import open_weather_token
from datetime import datetime


# @dp.message_handler(content_types=['location'])
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


def register_handlers_location_weather(dp: Dispatcher):
    dp.register_message_handler(
        get_location_weather, content_types=['location']
    )
