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
        'date': str(datetime.fromtimestamp(data['list'][0]['dt']))[:10],
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
        'date': str(datetime.fromtimestamp(data['list'][10]['dt']))[:10],
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
        'date': str(datetime.fromtimestamp(data['list'][18]['dt']))[:10],
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
        'date': str(datetime.fromtimestamp(data['list'][26]['dt']))[:10],
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
        'date': str(datetime.fromtimestamp(data['list'][34]['dt']))[:10],
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