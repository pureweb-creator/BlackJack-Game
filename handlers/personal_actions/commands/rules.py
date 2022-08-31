from aiogram import types
from dispatcher import dp
from dispatcher import game_controls
from dispatcher import db

# get rules command
@dp.message_handler(commands=['rules'])
async def rules(message: types.Message):
    lang = db.get('lang', message.from_user.id)['lang']
    _ = game_controls.get_locale(lang)
    await message.answer(_("""♦️ <b>Правила игры в Блэк-Джек (двадцать одно)</b> ♦️\n
Мы предоставим краткий свод правил для тех, кто никогда не играл в блэкджек.\n
Магическое число для блэкджека — 21.\nЗначения всех карт, розданных игроку, складываются, и если сумма превышает 21, игрок вылетает и мгновенно проигрывает.\n
Если игрок получает ровно 21, игрок выигрывает у дилера.\nВ противном случае для выигрыша сумма карт игрока должна быть больше суммы карт дилера.\n
Стоимости карт:
- Валет - 2 очка;\n- Дама - 3 очка;\n- Король - 4 очка;\n- Туз - 11 очков (если сумма карт больше 21, может стоить 1 очко);\nСтоимость остальных карт определяется их номиналом."""))
