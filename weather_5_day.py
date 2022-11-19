import requests

from decouple import config
from datetime import datetime


def get_weather(city, weather_toke):

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

    request = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?q='
                           f'{city}&appid={weather_toke}&units=metric')
    data = request.json()

    day_1 = {
        'city': data['city']['name'],
        'date': str(datetime.fromtimestamp(data['list'][0]['dt'])),
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
        'date': str(datetime.fromtimestamp(data['list'][8]['dt'])),
        'humidity': data['list'][8]['main']['humidity'],
        'pressure': data['list'][8]['main']['pressure'],
        'temp': data['list'][8]['main']['temp'],
        'weather': data['list'][8]['weather'][0]['main'],
        'wind': data['list'][8]['wind']['speed'],
        'visibility': data['list'][8]['visibility'],
    }

    if day_2['weather'] in code_to_smile:
        wd_2 = code_to_smile[day_1['weather']]
    else:
        wd_2 = 'Глянь у вікно, не розумію що там за погода!'

    day_3 = {
        'city': data['city']['name'],
        'date': str(datetime.fromtimestamp(data['list'][16]['dt'])),
        'humidity': data['list'][16]['main']['humidity'],
        'pressure': data['list'][16]['main']['pressure'],
        'temp': data['list'][16]['main']['temp'],
        'weather': data['list'][16]['weather'][0]['main'],
        'wind': data['list'][16]['wind']['speed'],
        'visibility': data['list'][16]['visibility'],
    }

    if day_3['weather'] in code_to_smile:
        wd_3 = code_to_smile[day_1['weather']]
    else:
        wd_3 = 'Глянь у вікно, не розумію що там за погода!'

    day_4 = {
        'city': data['city']['name'],
        'date': str(datetime.fromtimestamp(data['list'][24]['dt'])),
        'humidity': data['list'][24]['main']['humidity'],
        'pressure': data['list'][24]['main']['pressure'],
        'temp': data['list'][24]['main']['temp'],
        'weather': data['list'][24]['weather'][0]['main'],
        'wind': data['list'][24]['wind']['speed'],
        'visibility': data['list'][24]['visibility'],
    }

    if day_4['weather'] in code_to_smile:
        wd_4 = code_to_smile[day_1['weather']]
    else:
        wd_4 = 'Глянь у вікно, не розумію що там за погода!'

    day_5 = {
        'city': data['city']['name'],
        'date': str(datetime.fromtimestamp(data['list'][32]['dt'])),
        'humidity': data['list'][32]['main']['humidity'],
        'pressure': data['list'][32]['main']['pressure'],
        'temp': data['list'][32]['main']['temp'],
        'weather': data['list'][32]['weather'][0]['main'],
        'wind': data['list'][32]['wind']['speed'],
        'visibility': data['list'][32]['visibility'],
    }

    if day_5['weather'] in code_to_smile:
        wd_5 = code_to_smile[day_1['weather']]
    else:
        wd_5 = 'Глянь у вікно, не розумію що там за погода!'

    print(f'###{day_1["date"]}###\n'
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


def main():

    weather_token = config('WEATHER_KEY')
    city = input('Введіть місто: ')
    get_weather(city, weather_token)


if __name__ == '__main__':
    main()