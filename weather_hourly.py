import requests

from decouple import config
from datetime import datetime


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

        city = data['city']['name']
        date = []
        humidity = []
        pressure = []
        temp = []
        weather = []
        wind = []
        visibility = []
        smail = []

        for item in data['list']:
            date.append(str(datetime.fromtimestamp(item['dt'])))
            humidity.append(item['main']['humidity'])
            pressure.append(item['main']['pressure'])
            temp.append(item['main']['temp'])
            weather.append(item['weather'][0]['main'])
            wind.append(item['wind']['speed'])
            visibility.append(item['visibility'])

        for i in weather:
            if i in code_to_smile:
                wd = code_to_smile[i]
                smail.append(wd)

        for num in range(8):
            print(
                f'### {date[num]} ###\n'
                f'Погода в місті: {city}\n'
                f'Температура: {temp[num]}C° {smail[num]}\n'
                f'Вологість: {humidity[num]}%\n'
                f'Тиск: {pressure[num]} мм.рт.ст\n'
                f'Вітер: {wind[num]} м/с\n'
                f'Видимість: {visibility[num]}\n\n'
                f'Гарного дня!'
            )

    except Exception as error:
        print(error)


def main():

    weather_token = config('WEATHER_KEY')
    # city = input('Введіть місто: ')
    get_weather('Жмеринка', weather_token)


if __name__ == '__main__':
    main()
