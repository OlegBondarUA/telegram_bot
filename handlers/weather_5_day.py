import requests

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from handlers.smile import code_to_smile
from create_bot import open_weather_token
from datetime import datetime


class WeatherForm(StatesGroup):
    city_for_five_day_weather = State()


# @dp.message_handler(text='Weather for 5 day')
async def weather_5_day(message: types.Message):
    await message.reply("Great! Now enter the name of the city or press /cancel"
                        " if you change your mind.")
    await WeatherForm.city_for_five_day_weather.set()


# @dp.message_handler(state=WeatherForm.city_for_five_day_weather)
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
                wd = "Look out the window, " \
                     "I don't understand what kind of weather it is!"

            result = (
                f'### {str(datetime.fromtimestamp(item["dt"]))[:10]} ###\n'
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
                            f'{weather[3]} {weather[4]}'
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


def register_handlers_weather_5_day(dp: Dispatcher):
    dp.register_message_handler(weather_5_day, text='Weather for 5 day')
    dp.register_message_handler(
        get_weathers, state=WeatherForm.city_for_five_day_weather
    )
