from aiogram import types
from dispatcher import dp
from dispatcher import game_controls

# stat command
@dp.message_handler(commands=['stat'])
async def statistics(message: types.Message):
    msg, markup = await game_controls.print_statistics(message.from_user.id, message.from_user.first_name)
    await message.answer(msg, reply_markup=markup)
  