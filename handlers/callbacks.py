from dispatcher import dp
from dispatcher import bot
from bot import db

@dp.callback_query_handler(lambda call: True)
async def callback_inline(call):
	try: 
		if call.message:
			if call.data == "lang_russian":
				db.update('user', 'lang = ?', 'user_id = ?', ('ru', call.from_user.id,))
				await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Язык успешно сменен!\nПерезапустить: /start", reply_markup=None)
			if call.data == "lang_english":
				db.update('user', 'lang = ?', 'user_id = ?', ('en', call.from_user.id,))
				await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Language successfully changed!\nReload bot: /start", reply_markup=None)
	except Exception as e:
		print(repr(e))