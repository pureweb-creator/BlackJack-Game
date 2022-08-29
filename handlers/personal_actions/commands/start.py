from aiogram import types
from dispatcher import dp
from dispatcher import game_controls, Keyboard
from dispatcher import db
import json
from datetime import datetime, timedelta

# start command 
@dp.message_handler(commands=['start'])
async def process_start_game(message: types.Message):
    '''bot start'''
    user = db.load_user(message.from_user.id)

    # register user if does not exist
    if (user==False):
        with open('static/deck_of_cards.json','r', encoding="utf-8") as input_f:
            deck = json.load(input_f)
        input_f.close()

        db.add_user(int(message.from_user.id), message.from_user.first_name, message.from_user.last_name, deck)
        
    user = db.load_user(message.from_user.id)
    _ = game_controls.get_locale(user['lang'])

    # keyboard
    kbd = Keyboard(user['lang'])
    main_menu_markup = kbd.new_game()

    # Getting the current date and time
    dt = datetime.utcnow()+timedelta(hours=3)

    db.update('users','is_game = %s, last_played = %s','user_id = %s',(False, dt, message.from_user.id,))
    await message.answer(_("♦️ Добро пожаловать в блэк-джек ♦️"), reply_markup=main_menu_markup)
