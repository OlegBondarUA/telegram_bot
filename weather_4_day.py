import json
import requests

from decouple import config
from datetime import datetime
from pprint import pprint

open_weather_token = config('WEATHER_KEY')


def get_weather(city, open_weather_toke):

    request = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?q='
                           f'{city}&appid={open_weather_token}&units=metric')
    data = request.json()

    day_1 = {
        'city': data['city']['name'],
        'date_time': str(datetime.fromtimestamp(data['list'][0]['dt']))[:10],
        'humidity': data['list'][0]['main']['humidity'],
        'pressure': data['list'][0]['main']['pressure'],
        'temp': data['list'][0]['main']['temp'],
        'weather': data['list'][0]['weather'][0]['description'],
        'wind': data['list'][0]['wind']['speed'],
        'visibility': data['list'][0]['visibility'],
    }

    day_2 = {
        'city': data['city']['name'],
        'date_time': str(datetime.fromtimestamp(data['list'][10]['dt']))[:10],
        'humidity': data['list'][10]['main']['humidity'],
        'pressure': data['list'][10]['main']['pressure'],
        'temp': data['list'][10]['main']['temp'],
        'weather': data['list'][10]['weather'][0]['description'],
        'wind': data['list'][10]['wind']['speed'],
        'visibility': data['list'][10]['visibility'],
    }

    day_3 = {
        'city': data['city']['name'],
        'date_time': str(datetime.fromtimestamp(data['list'][18]['dt']))[:10],
        'humidity': data['list'][18]['main']['humidity'],
        'pressure': data['list'][18]['main']['pressure'],
        'temp': data['list'][18]['main']['temp'],
        'weather': data['list'][18]['weather'][0]['description'],
        'wind': data['list'][18]['wind']['speed'],
        'visibility': data['list'][18]['visibility'],
    }

    day_4 = {
        'city': data['city']['name'],
        'date_time': str(datetime.fromtimestamp(data['list'][26]['dt']))[:10],
        'humidity': data['list'][26]['main']['humidity'],
        'pressure': data['list'][26]['main']['pressure'],
        'temp': data['list'][26]['main']['temp'],
        'weather': data['list'][26]['weather'][0]['description'],
        'wind': data['list'][26]['wind']['speed'],
        'visibility': data['list'][26]['visibility'],
    }

    day_5 = {
        'city': data['city']['name'],
        'date_time': str(datetime.fromtimestamp(data['list'][34]['dt']))[:10],
        'humidity': data['list'][34]['main']['humidity'],
        'pressure': data['list'][34]['main']['pressure'],
        'temp': data['list'][34]['main']['temp'],
        'weather': data['list'][34]['weather'][0]['description'],
        'wind': data['list'][34]['wind']['speed'],
        'visibility': data['list'][34]['visibility'],
    }
    pprint(day_1)
    pprint(day_2)
    pprint(day_3)
    pprint(day_4)
    pprint(day_5)


def main():
    city = input('Введіть місто: ')
    get_weather(city, open_weather_token)


if __name__ == '__main__':
    main()