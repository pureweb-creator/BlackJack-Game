from aiogram import types
from dispatcher import dp
from dispatcher import Game_controls
from dispatcher import db

game_controls = Game_controls()

# get balance command
@dp.message_handler(commands=['balance'])
async def get_balance(message: types.Message):
    user = db.load_user(message.from_user.id)
    _ = game_controls.get_locale(user['lang'])

    await message.answer(_("💰 Баланс: ")+ str(user['balance']))
