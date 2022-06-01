from dispatcher import dp
from dispatcher import bot
from bot import db
from game_controls import Game_controls
from aiogram import types

@dp.callback_query_handler(lambda call: True)
async def callback_inline(call):
	try:
		if call.message:
			user = db.load_user(call.from_user.id)

			# get current user locale
			locale = Game_controls()
			_ = locale.get_locale(user['lang'])

			if call.data == "lang_russian":
				db.update('users', 'lang = %s', 'user_id = %s', ('ru', call.from_user.id,))
				await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Язык успешно сменен!\nНужно перезапустить, чтоб изменения вступили в силу: /start", reply_markup=None)
			
			if call.data == "lang_english":
				db.update('users', 'lang = %s', 'user_id = %s', ('en', call.from_user.id,))
				await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Language successfully changed!\nReload bot to apply changes: /start", reply_markup=None)
			
			if call.data == "change_lang":
				# keyboard
				russian_lang_btn = types.InlineKeyboardButton('Русский 🇷🇺', callback_data='lang_russian')
				eng_lang_btn = types.InlineKeyboardButton('English 🇺🇸', callback_data='lang_english')
				back_to_main_btn = types.InlineKeyboardButton(_("◀️ Назад"), callback_data='back_to_main')
				change_lang_markup = types.InlineKeyboardMarkup(row_width=2).add(russian_lang_btn, eng_lang_btn, back_to_main_btn)

				await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="<b>"+_("Настройки 🛠 — Сменить язык 👅")+"</b>", reply_markup=change_lang_markup)
			
			if call.data == "contact_support":
				# keyboard
				btn1 = types.InlineKeyboardButton(text=_("⚡️ Связаться с разработчиком ⚡️"), url="https://t.me/bug_lag_feature")
				btn2 = types.InlineKeyboardButton(_("◀️ Назад"), callback_data='back_to_main')
				markup = types.InlineKeyboardMarkup(row_width=1).add(btn1, btn2)

				await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="<b>"+_("Настройки 🛠 — Тех поддержка 👨‍💻")+"</b>", reply_markup=markup)
			
			if call.data == "back_to_main":
				btn1 = types.InlineKeyboardButton(_('Сменить язык 👅'), callback_data="change_lang")
				btn2 = types.InlineKeyboardButton(_('Тех поддержка 👨‍💻'), callback_data="contact_support")
				settings_markup = types.InlineKeyboardMarkup().add(btn1, btn2)
				await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="<b>"+_("Настройки 🛠")+"</b>", reply_markup=settings_markup)

			# confirmation message for clear statistics action
			if call.data == "confirmation":
				btn1 = types.InlineKeyboardButton(_("Да 🆗"), callback_data="clear_statistics")
				btn2 = types.InlineKeyboardButton(_("Отмена 🙅‍♂️"), callback_data="back_to_statistics")
				confirmation_markup = types.InlineKeyboardMarkup().add(btn1, btn2)
				await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="<b>"+_("Вы уверены? Это приведет к полной потере всех ваших данных!")+"</b>", reply_markup=confirmation_markup)

			if call.data == "back_to_statistics":
				stat = Game_controls()
				msg, markup = await stat.print_statistics(call.from_user.id, call.from_user.first_name)
				await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg, reply_markup=markup)

			if call.data == "clear_statistics":
				db.update("users", "games_played = %s, games_won = %s, games_lost = %s, games_tied = %s, max_win = %s, max_loss = %s, all_in_games_count = %s, all_in_win = %s, all_in_loss = %s, all_in_tie = %s", "user_id = %s, blackjack_count = %s", (0,0,0,0,0,0,0,0,0,0,0, call.message.chat.id))

				stat = Game_controls()
				msg, markup = await stat.print_statistics(call.from_user.id, call.from_user.first_name)
				await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg, reply_markup=markup)				
	except Exception as e:
		print(repr(e))