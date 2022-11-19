import requests
import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

from decouple import config


open_weather_token = config('WEATHER_KEY')
tg_bot_token = config('TELEGRAM_TOKEN')
bot = Bot(token=tg_bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class InputFSM(StatesGroup):
    input_weather = State()


@dp.message_handler(commands=['start'])
async def Start_command(message: types.Message):
    kb = [
        [types.KeyboardButton(text="На 1 день")],
        [types.KeyboardButton(text="На 5 днів")]
        ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )

    await message.reply('Привіт! Вибери на скільки днів ти '
                        'хочеш дізнатися погоду', reply_markup=keyboard)


@dp.message_handler(text="На 1 день")
async def weather_1_day(message: types.Message):
    await message.answer("Відмінний вибір!, Введи назву міста")
    await InputFSM.input_weather.set()

    @dp.message_handler(state=InputFSM.input_weather)
    async def get_weather(message: types.Message, state: FSMContext):
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
                f'&appid={open_weather_token}&units=metric'
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
            await state.finish()
        except Exception:
            await message.reply('\U00002620Перевірте назву міста\U00002620')


@dp.message_handler(text="На 5 днів")
async def weather_5_day(message: types.Message):
    await message.reply("Введи назву міста")
    await InputFSM.input_weather.set()

    @dp.message_handler(state=InputFSM.input_weather)
    async def get_weathers(message: types.Message, state: FSMContext):
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

        try:
            request = requests.get(
                f'https://api.openweathermap.org/data/2.5/forecast?q='
                f'{message.text}&appid={open_weather_token}&units=metric')
            data = request.json()

            day_1 = {
                'city': data['city']['name'],
                'date': str(datetime.datetime.fromtimestamp(data['list'][0]['dt']))[:10],
                'humidity': data['list'][0]['main']['humidity'],
                'pressure': data['list'][0]['main']['pressure'],
                'temp': data['list'][0]['main']['temp'],
                'weather': data['list'][0]['weather'][0]['main'],
                'wind': data['list'][0]['wind']['speed'],
                'visibility': data['list'][0]['visibility'],
            }

            if day_1['weather'] in code_to_smile:
                wd = code_to_smile[day_1['weather']]
            else:
                wd = 'Глянь у вікно, не розумію що там за погода!'

            day_2 = {
                'city': data['city']['name'],
                'date': str(datetime.datetime.fromtimestamp(data['list'][10]['dt']))[:10],
                'humidity': data['list'][10]['main']['humidity'],
                'pressure': data['list'][10]['main']['pressure'],
                'temp': data['list'][10]['main']['temp'],
                'weather': data['list'][10]['weather'][0]['main'],
                'wind': data['list'][10]['wind']['speed'],
                'visibility': data['list'][10]['visibility'],
            }

            if day_2['weather'] in code_to_smile:
                wd_2 = code_to_smile[day_1['weather']]
            else:
                wd_2 = 'Глянь у вікно, не розумію що там за погода!'

            day_3 = {
                'city': data['city']['name'],
                'date': str(datetime.datetime.fromtimestamp(data['list'][18]['dt']))[:10],
                'humidity': data['list'][18]['main']['humidity'],
                'pressure': data['list'][18]['main']['pressure'],
                'temp': data['list'][18]['main']['temp'],
                'weather': data['list'][18]['weather'][0]['main'],
                'wind': data['list'][18]['wind']['speed'],
                'visibility': data['list'][18]['visibility'],
            }

            if day_3['weather'] in code_to_smile:
                wd_3 = code_to_smile[day_1['weather']]
            else:
                wd_3 = 'Глянь у вікно, не розумію що там за погода!'

            day_4 = {
                'city': data['city']['name'],
                'date': str(datetime.datetime.fromtimestamp(data['list'][26]['dt']))[:10],
                'humidity': data['list'][26]['main']['humidity'],
                'pressure': data['list'][26]['main']['pressure'],
                'temp': data['list'][26]['main']['temp'],
                'weather': data['list'][26]['weather'][0]['main'],
                'wind': data['list'][26]['wind']['speed'],
                'visibility': data['list'][26]['visibility'],
            }

            if day_4['weather'] in code_to_smile:
                wd_4 = code_to_smile[day_1['weather']]
            else:
                wd_4 = 'Глянь у вікно, не розумію що там за погода!'

            day_5 = {
                'city': data['city']['name'],
                'date': str(datetime.datetime.fromtimestamp(data['list'][34]['dt']))[:10],
                'humidity': data['list'][34]['main']['humidity'],
                'pressure': data['list'][34]['main']['pressure'],
                'temp': data['list'][34]['main']['temp'],
                'weather': data['list'][34]['weather'][0]['main'],
                'wind': data['list'][34]['wind']['speed'],
                'visibility': data['list'][34]['visibility'],
            }

            if day_5['weather'] in code_to_smile:
                wd_5 = code_to_smile[day_1['weather']]
            else:
                wd_5 = 'Глянь у вікно, не розумію що там за погода!'

            await message.reply(
                f'###{day_1["date"]}###\n'
                f'Погода в місті: {day_1["city"]}\nТемпература: {day_1["temp"]}C° {wd}\n'
                f'Вологість: {day_1["humidity"]}%\nТиск: {day_1["pressure"]} мм.рт.ст\n'
                f'Вітер: {day_1["wind"]} м/с\n'
                f'Видимість: {day_1["visibility"]}\n\n'
                f'###{day_2["date"]}###\n'
                f'Погода в місті: {day_2["city"]}\nТемпература: {day_2["temp"]}C° {wd_2}\n'
                f'Вологість: {day_2["humidity"]}%\nТиск: {day_2["pressure"]} мм.рт.ст\n'
                f'Вітер: {day_2["wind"]} м/с\n'
                f'Видимість: {day_2["visibility"]}\n\n'
                f'###{day_3["date"]}###\n'
                f'Погода в місті: {day_3["city"]}\nТемпература: {day_3["temp"]}C° {wd_3}\n'
                f'Вологість: {day_3["humidity"]}%\nТиск: {day_3["pressure"]} мм.рт.ст\n'
                f'Вітер: {day_3["wind"]} м/с\n'
                f'Видимість: {day_3["visibility"]}\n\n'
                f'###{day_4["date"]}###\n'
                f'Погода в місті: {day_4["city"]}\nТемпература: {day_4["temp"]}C° {wd_4}\n'
                f'Вологість: {day_4["humidity"]}%\nТиск: {day_4["pressure"]} мм.рт.ст\n'
                f'Вітер: {day_4["wind"]} м/с\n'
                f'Видимість: {day_4["visibility"]}\n\n'
                f'###{day_5["date"]}###\n'
                f'Погода в місті: {day_5["city"]}\nТемпература: {day_5["temp"]}C° {wd_5}\n'
                f'Вологість: {day_5["humidity"]}%\nТиск: {day_5["pressure"]} мм.рт.ст\n'
                f'Вітер: {day_5["wind"]} м/с\n'
                f'Видимість: {day_5["visibility"]}\n\n'
                f'Гарного дня!')
            await state.finish()
        except Exception:
            await message.reply('\U00002620Перевірте назву міста\U00002620')


if __name__ == '__main__':
    executor.start_polling(dp)
