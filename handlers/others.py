from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup

from table_for_bot import User, Message


class WeatherForm(StatesGroup):
    message_client = State()


# @dp.message_handler(text='The official weather source')
async def official_source(message):
    await message.answer('https://openweathermap.org/'
                         '\n\nHave a nice day!'
                         '\nTo request the weather again, press /begin\n',
                         reply_markup=types.ReplyKeyboardRemove()
                         )


# @dp.message_handler(text='Пропозиції для розвитку!')
async def message_acceptance(message: types.Message):
    await message.reply('Чудово розкажіть нам про помилку у роботі бота'
                        ' або запропонуйте нам щось. Що би ви хотіли '
                        'бачити в цьому боті.')
    await WeatherForm.message_client.set()


# @dp.message_handler(state=WeatherForm.message_client)
async def message_save(message: types.Message):

    us = User.get_or_create(
        user_name=str(message['chat']['username']),
        chat_id=int(message['chat']['id'])
    )

    mes = Message.create(
        message=str(message['text']),
        chat_id=int(message['chat']['id'])
    )

    await message.reply('Дякую за ваш відгук!'
                        '\nTo request the weather again, press /begin\n',
                        reply_markup=types.ReplyKeyboardRemove()
                        )

    return us, mes


def register_handlers_others(dp: Dispatcher):
    dp.register_message_handler(
        official_source, text='The official weather source'
    )
    dp.register_message_handler(
        message_acceptance, text='Пропозиції для розвитку!'
    )
    dp.register_message_handler(
        message_save, state=WeatherForm.message_client
    )

