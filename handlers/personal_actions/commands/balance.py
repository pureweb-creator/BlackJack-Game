from aiogram import types
from dispatcher import dp
from dispatcher import Game_controls
from dispatcher import db

game_controls = Game_controls()

# get balance command
@dp.message_handler(commands=['balance'])
async def get_balance(message: types.Message):
    lang = db.get('lang', message.from_user.id)['lang']
    balance = db.get('balance', message.from_user.id)['balance']
    _ = game_controls.get_locale(lang)

    await message.answer(_("💰 Баланс: ")+ str(balance))
