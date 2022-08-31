from aiogram import types
from dispatcher import dp
from dispatcher import game_controls
from dispatcher import db

# change lang command
@dp.message_handler(commands=['lang'])
async def change_lang(message: types.Message):
    lang = db.get('lang', message.from_user.id)['lang']

    # get current user locale
    _ = game_controls.get_locale(lang)
    
    # keyboard
    russian_lang_btn = types.InlineKeyboardButton('Русский 🇷🇺', callback_data='lang_russian')
    eng_lang_btn = types.InlineKeyboardButton('English 🇺🇸', callback_data='lang_english')
    change_lang_markup = types.InlineKeyboardMarkup().add(russian_lang_btn, eng_lang_btn)

    await message.answer(_("Выберите язык"), reply_markup=change_lang_markup)
