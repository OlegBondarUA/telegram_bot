import requests

from decouple import config
from datetime import datetime


def get_weather(city, weather_toke):
    try:
        request = requests.get(f'https://api.openweathermap.org/data/2.5/'
                               f'forecast?q={city}&appid={weather_toke}&units=metric')

        data = request.json()

        for num in range(8):
            print(
                f'### {str(datetime.fromtimestamp(data["list"][num]["dt"]))} ###\n'
                f'Погода в місті: {data["city"]["name"]}\n'
                f'Температура: {data["list"][num]["main"]["temp"]}C°\n'
                f'Вологість: {data["list"][num]["main"]["humidity"]}%\n'
                f'Тиск: {data["list"][num]["main"]["pressure"]} мм.рт.ст\n'
                f'Вітер: {data["list"][num]["wind"]["speed"]} м/с\n'
                f'Видимість: {data["list"][num]["visibility"]}\n\n'
            )
        print('Гарного дня!')

    except Exception as error:
        print(error)


def main():

    weather_token = config('WEATHER_KEY')
    # city = input('Введіть місто: ')
    get_weather('Жмеринка', weather_token)


if __name__ == '__main__':
    main()
