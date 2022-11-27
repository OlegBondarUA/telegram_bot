import requests

from decouple import config
from datetime import datetime
from pprint import pprint


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


def get_weather(city, weather_toke):
    try:
        request = requests.get(f'https://api.openweathermap.org/data/2.5/'
                               f'forecast?q={city}&appid={weather_toke}&units=metric')

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
                f'{wd}\n'
                f'Вологість: {item["main"]["humidity"]}%\n'
                f'Тиск: {item["main"]["pressure"]} мм.рт.ст\n'
                f'Вітер: {item["wind"]["speed"]} м/с\n'
                f'Видимість: {item["visibility"]}\n\n'
            )
            weather.append(result)
        pprint(weather)
        print('Гарного дня!')

    except Exception as error:
        print(error)


def main():

    weather_token = config('WEATHER_KEY')
    city = input('Введіть місто: ')
    get_weather(city, weather_token)


if __name__ == '__main__':
    main()
