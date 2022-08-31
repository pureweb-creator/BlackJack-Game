from aiogram import types
from dispatcher import dp
from dispatcher import game_controls
from dispatcher import db

# settings command
@dp.message_handler(commands=['share'])
async def settigns(message: types.Message):
    # get current user locale
    lang = db.get('lang', message.from_user.id)['lang']
    _ = game_controls.get_locale(lang)

    # keyboard
    btn = types.InlineKeyboardButton(_("Выбрать чат")+" 💬", switch_inline_query="\n"+_("Приглашаю тебя в BlackJack!")+" 🃏\n⬆️⬆️")
    markup = types.InlineKeyboardMarkup().add(btn)

    await message.answer("🔽 "+_("Нажмите на кнопку ниже для того, чтобы отправить бота другу"), reply_markup=markup)
