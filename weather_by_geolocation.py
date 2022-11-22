import datetime
import requests
from decouple import config

open_weather_token = config('WEATHER_KEY')
lat = '50.4547'
lon = '30.5238'

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


def get_weather(latitude, longitude, open_weather_toke):

    request = requests.get(f'https://api.openweathermap.org/data/2.5/weather?'
                           f'lat={latitude}&lon={longitude}&appid={open_weather_toke}')

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
        datetime.datetime.fromtimestamp(data['sys']['sunrise'])
    sunset_timestamp = \
        datetime.datetime.fromtimestamp(data['sys']['sunset'])
    length_of_the_day = \
        datetime.datetime.fromtimestamp(data['sys']['sunset']) - \
        datetime.datetime.fromtimestamp(data['sys']['sunrise'])

    print(f'### {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")} ###\n'
          f'Погода в місті: {city}\n'
          f'Температура: {float("{:.1f}".format(cur_weather))}C° {wd}\n'
          f'Вологість: {humidity}%\nТиск: {pressure} мм.рт.ст\n'
          f'Вітер: {wind} м/с\nСхід сонця: {sunrise_timestamp}\n'
          f'Захід сонця: {sunset_timestamp}\n'
          f'Тривалість дня: {length_of_the_day}\n'
          f'Гарного дня!')


def main():

    get_weather(lat, lon, open_weather_token)


if __name__ == '__main__':
    main()
