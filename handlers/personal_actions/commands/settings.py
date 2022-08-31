from aiogram import types
from dispatcher import dp
from dispatcher import game_controls
from dispatcher import db

# settings command
@dp.message_handler(commands=['settings'])
async def settigns(message: types.Message):
    # get current user locale
    lang = db.get('lang', message.from_user.id)['lang']
    _ = game_controls.get_locale(lang)

    # keyboard
    btn1 = types.InlineKeyboardButton(_('Сменить язык 👅'), callback_data="change_lang")
    btn2 = types.InlineKeyboardButton(_('Тех поддержка 👨‍💻'), callback_data="contact_support")
    settings_markup = types.InlineKeyboardMarkup().add(btn1, btn2)

    await message.answer("<b>"+_("Настройки 🛠")+"</b>", reply_markup=settings_markup)
