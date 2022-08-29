from aiogram import types
from dispatcher import dp
from dispatcher import game_controls
from dispatcher import db
from config import DEV_CONTACT

# get help command
@dp.message_handler(commands=['help'])
async def info_help(message: types.Message):
    user = db.load_user(message.from_user.id)
    _ = game_controls.get_locale(user['lang'])
    await message.answer(_("Связаться с разработчиком: {}").format(DEV_CONTACT))
