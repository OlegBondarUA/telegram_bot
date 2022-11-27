from aiogram.utils import executor

from create_bot import dp
from handlers import (
    commands,
    weather_1_day,
    weather_5_day,
    weather_hourly,
    weather_by_geolocation,
    others
)


commands.register_handlers_commands(dp)
weather_1_day.register_handlers_weather_1_day(dp)
weather_5_day.register_handlers_weather_5_day(dp)
weather_hourly.register_handlers_hourly_weathers(dp)
weather_by_geolocation.register_handlers_location_weather(dp)
others.register_handlers_others(dp)

    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
