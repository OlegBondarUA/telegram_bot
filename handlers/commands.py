import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext


# @dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Hello! I'm a weather bot, I can tell you what the "
                        "weather will be like elsewhere.\nTo start work, "
                        "enter the command /begin")


# @dp.message_handler(commands=['begin'])
async def begin_command(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Weather for 1 day")] +
        [types.KeyboardButton(text="Weather for 5 day")] +
        [types.KeyboardButton(text="Hourly weather")],
        [types.KeyboardButton(text="Geolocation weather", request_location=True)],
        [types.KeyboardButton(text="The official weather source")] +
        [types.KeyboardButton(text="Пропозиції для розвитку!")]
        ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )

    await message.reply('Choose your weather option '
                        'and click on the button below.', reply_markup=keyboard)


# @dp.message_handler(commands=['cancel'])
async def cancel_command(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    logging.info('Cancelling state %r', current_state)
    await state.finish()
    await message.answer('We entered the /cancel command',
                         reply_markup=types.ReplyKeyboardRemove())


def register_handlers_commands(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(begin_command, commands=['begin'])
    dp.register_message_handler(cancel_command, commands=['cancel'])
