import json
import random

from aiogram import types
from dispatcher import dp
from dispatcher import bot
from dispatcher import config
from bot import db

from datetime import datetime, timedelta
from game_controls import Game_controls, Keyboard
from config import STICKERS

dealer_score = 0
game_controls = Game_controls()
global _

# settings command
@dp.message_handler(commands=['settings'])
async def settigns(message: types.Message):
    # get current user locale
    user = db.load_user(message.from_user.id)
    _ = game_controls.get_locale(user['lang'])

    # keyboard
    btn1 = types.InlineKeyboardButton(_('Сменить язык 👅'), callback_data="change_lang")
    btn2 = types.InlineKeyboardButton(_('Тех поддержка 👨‍💻'), callback_data="contact_support")
    settings_markup = types.InlineKeyboardMarkup().add(btn1, btn2)

    await message.answer("<b>"+_("Настройки 🛠")+"</b>", reply_markup=settings_markup)

# stat command
@dp.message_handler(commands=['stat'])
async def statistics(message: types.Message):
    msg, markup = await game_controls.print_statistics(message.from_user.id, message.from_user.first_name)
    await message.answer(msg, reply_markup=markup)
    
# get help command
@dp.message_handler(commands=['help'])
async def info_help(message: types.Message):
    user = db.load_user(message.from_user.id)
    _ = game_controls.get_locale(user['lang'])
    await message.answer(_("Связаться с разработчиком: @i_suss"))

# get balance command
@dp.message_handler(commands=['balance'])
async def get_balance(message: types.Message):
    user = db.load_user(message.from_user.id)
    _ = game_controls.get_locale(user['lang'])

    await message.answer(_("💰 Баланс: ")+ str(user['balance']))

# change lang command
@dp.message_handler(commands=['lang'])
async def change_lang(message: types.Message):
    user = db.load_user(message.from_user.id)

    # get current user locale
    _ = game_controls.get_locale(user['lang'])
    
    # keyboard
    russian_lang_btn = types.InlineKeyboardButton('Русский 🇷🇺', callback_data='lang_russian')
    eng_lang_btn = types.InlineKeyboardButton('English 🇺🇸', callback_data='lang_english')
    change_lang_markup = types.InlineKeyboardMarkup().add(russian_lang_btn, eng_lang_btn)

    await message.answer(_("Выберите язык"), reply_markup=change_lang_markup)

# get rules command
@dp.message_handler(commands=['rules'])
async def rules(message: types.Message):
    user = db.load_user(message.from_user.id)
    _ = game_controls.get_locale(user['lang'])
    await message.answer(_("""♦️ <b>Правила игры в Блэк-Джек (двадцать одно)</b> ♦️\n
Мы предоставим краткий свод правил для тех, кто никогда не играл в блэкджек.\n
Магическое число для блэкджека — 21.\nЗначения всех карт, розданных игроку, складываются, и если сумма превышает 21, игрок вылетает и мгновенно проигрывает.\n
Если игрок получает ровно 21, игрок выигрывает у дилера.\nВ противном случае для выигрыша сумма карт игрока должна быть больше суммы карт дилера.\n
Стоимости карт:
- Валет - 2 очка;\n- Дама - 3 очка;\n- Король - 4 очка;\n- Туз - 11 очков (если сумма карт больше 21, может стоить 1 очко);\nСтоимость остальных карт определяется их номиналом."""))

# start command 
@dp.message_handler(commands=['start'])
async def process_start_game(message: types.Message):
    '''bot start'''
    user = db.load_user(message.from_user.id)
    if (user==False):
        # register user if not exists
        test = db.add_user(int(message.from_user.id), message.from_user.first_name, message.from_user.last_name)

    user = db.load_user(message.from_user.id)
    _ = game_controls.get_locale(user['lang'])

    # keyboard
    kbd = Keyboard(user['lang'])
    main_menu_markup = kbd.new_game()

    # Getting the current date and time
    dt = datetime.utcnow()+timedelta(hours=3)

    db.update('users','is_game = %s, last_played = %s','user_id = %s',(False, dt, message.from_user.id,))
    await message.answer(_("♦️ Добро пожаловать в блэк-джек ♦️"), reply_markup=main_menu_markup)

# main game logic
@dp.message_handler(content_types=["text"])
async def process_handler(message: types.Message):
    '''button handlers'''
    global is_all_in
    
    is_all_in  = False # variable for check below in statistics. Default false
    user = db.load_user(message.from_user.id)

    # global declaration
    kbd = Keyboard(user['lang'])
    _ = game_controls.get_locale(user['lang'])

    if message.text == _("Начать новую игру 🎮"):
        user = db.load_user(message.from_user.id)

        # updating deck of cards
        with open('static/deck_of_cards.json','r', encoding="utf-8") as input_f:
            deck = json.load(input_f)
        input_f.close()

        db.update(table='users', set='deck = %s, user_nickname = %s', where='user_id = %s', values=(str(deck), message.from_user.username, message.from_user.id,))

        # Getting the current date and time
        dt = datetime.utcnow()+timedelta(hours=3)

        # update player score is he lost everything
        if user['balance'] < 1:
            user['balance'] = 100
            db.update(table='users', set='balance = %s, is_game = %s, last_played = %s', where='user_id = %s', values=(100, True, dt, message.from_user.id,))
        else: db.update(table='users', set='is_game = %s, last_played = %s', where='user_id = %s', values=(True, dt, message.from_user.id,))

        # keyboard
        game_type_markup = kbd.game_type()

        # choose random sticker
        sticker_hash = random.choice(STICKERS)
        await bot.send_sticker(message.chat.id, sticker_hash)
        await message.answer(_("Выберите тип игры"), reply_markup=game_type_markup)

    if message.text == _("Играть с компьютером 🧠"):
        user = db.load_user(message.from_user.id)
        if (user['is_game'] == False):
            await message.answer(_("Для начала начните новую игру"))
            return;

        # keyboard
        choose_bet_markup = kbd.bet(user)
        await message.answer(_("Сделайте ставку"), reply_markup=choose_bet_markup)

    # When player chosed bet, we can start a new game
    if ("🪙" in message.text or _("Ва-банк! 🤑") in message.text):
        # basic check
        user = db.load_user(message.from_user.id)
        if (user['is_game'] == False):
            await message.answer(_("Для начала начните новую игру"))
            return;

        # reset all our local variables
        global dealer_score, player_score, player_cards, dealer_cards, bet
        deck         = []
        dealer_cards = []
        player_cards = []
        player_score = 0
        dealer_score = 0
        deck         = list(eval(user['deck']))

        # render keyboard
        game_controls_markup = kbd.game_nav_1()
        
        # save in db if player chosed All-in game
        if (_("Ва-банк! 🤑") in message.text):
            bet = user['balance']
            db.update('users','is_all_in = %s', 'user_id = %s', (True, message.from_user.id))
        else:
            bet = message.text.split()[0]
            db.update('users','is_all_in = %s', 'user_id = %s', (False, message.from_user.id))

        # update bet in db
        db.update(table='users', set='bet = %s',where='user_id = %s', values=(bet, message.from_user.id,))
        # and load
        user = db.load_user(message.from_user.id)
        is_all_in = user['is_all_in'] # true if player chosed All in, or False if not

        # basic check 
        if (int(bet) > int(user['balance'])):
            await message.answer(_("На вашем балансе недостаточно средств."))
            return

        # show message
        await message.answer(_("Ставка в {} принята.🤑 Приятной игры!").format(message.text))
        
        # Initial dealing. Two cards for both
        for i in range(2):
            # for player
            player_card = random.choice(deck)
            player_cards.append(player_card)
            deck.remove(player_card)
            player_score += player_card.get('cost')

            # for dealer
            dealer_card = random.choice(deck)
            dealer_cards.append(dealer_card)
            deck.remove(dealer_card)
            dealer_score += dealer_card.get('cost')

        # if both cards are Ace for player
        if player_cards[0].get('cost') == 11 and player_cards[1].get('cost') == 11:
            player_cards[0]['cost'] = 1
            player_score -= 10

        # if both cards are Ace for dealer
        if dealer_cards[0].get('cost') == 11 and dealer_cards[1].get('cost') == 11:
            dealer_cards[0]['cost'] = 1
            dealer_score -= 10

        db.update(table='users', set='player_score = %s, deck = %s, player_cards = %s, dealer_cards = %s, dealer_score = %s', where='user_id = %s', values=(player_score, str(deck), str(player_cards), str(dealer_cards), dealer_score, message.from_user.id,))

        # render dealer hided cards
        game_controls.render_cards([dealer_cards[0]['image'], 'static/images/back.png'], 2, f"{message.from_user.id}_out_dealer_close.webp")
        # render player cards
        game_controls.render_cards([player_cards[0]['image'], player_cards[1]['image']], 2, f"{message.from_user.id}_out_player.webp")
    
        # print dealer cards and score          
        await bot.send_sticker(message.chat.id, sticker=open(f"static/images/{message.from_user.id}_out_dealer_close.webp", 'rb').read())
        await message.answer("⬆️ 👽 <b>"+_("Карты дилера")+": </b>"+_("Скрыто"))

        # print player cards and score
        await bot.send_sticker(message.chat.id, sticker=open(f"static/images/{message.from_user.id}_out_player.webp", 'rb').read())
        user = db.load_user(message.from_user.id)
        await message.answer("⬆️ 👨‍💼 <b>"+_("Ваши карты")+f": </b> {user['player_score']}", reply_markup=game_controls_markup)

        # Player gets a blackjack (WIN)
        if (player_score == 21):
            # set a keyboard
            main_menu_markup = kbd.new_game()
            
            # updating player score
            current_win = float(bet)*float(1.5)
            total_win = current_win+user['balance']
            
            # updates a lot of data in database
            game_controls.collect_statistics(
                message.from_user.id,
                game_result=config.GAME_WIN,
                balance=total_win,
                current_win=current_win,
                is_all_in=is_all_in,
                is_blackjack = True
            )
            
            # pring player cards and score
            await message.answer(_("У вас Блэк-Джек! Вы победили!")+" 🥃\n<b>"+_("Чистый выигрыш")+f"</b>: {current_win} 💴", reply_markup=main_menu_markup)

    # if player decides to go on
    if (message.text == _("Еще 🟢")):
        # load from db
        user         = db.load_user(message.from_user.id)
        dealer_cards = list(eval(user['dealer_cards']))
        player_cards = list(eval(user['player_cards']))
        deck         = list(eval(user['deck']))
        is_all_in    = user['is_all_in']

        # basic check 
        if (user['is_game'] == False):
            await message.answer(_("Для начала начните новую игру"))
            return;

        # randomly dealing a card for player
        player_card = random.choice(deck)
        player_cards.append(player_card)
        deck.remove(player_card)
        user['player_score'] += player_card.get('cost')

        db.update(table='users', set='player_score = %s, deck = %s, player_cards = %s', where='user_id = %s', values=(str(user['player_score']), str(deck), str(player_cards), message.from_user.id, ))

        # generate image
        img_path = []
        for i in range(len(player_cards)):
            img_path.append(player_cards[i]['image'])
        
        # render player cards
        game_controls.render_cards(img_path, len(player_cards), f"{message.from_user.id}_out_player.webp")
        # render dealer hided cards
        game_controls.render_cards([dealer_cards[0]['image'], 'static/images/back.png'], 2, f"{message.from_user.id}_out_dealer_close.webp")
        # render dealer revealed cards
        game_controls.render_cards([dealer_cards[0]['image'], dealer_cards[1]['image']], 2, f"{message.from_user.id}_out_dealer_open.webp")

        # set a keyboard
        continue_game_controls_markup = kbd.game_nav_2()   

        # if player wons
        if (user['player_score'] == 21):
            current_win = float(user['bet'])*float(1.5)
            total_win = current_win+user['balance'] # update win

            # print dealer cards and score
            await bot.send_sticker(message.chat.id, sticker=open(f"static/images/{message.from_user.id}_out_dealer_open.webp", 'rb').read())
            user = db.load_user(message.from_user.id)
            await message.answer(f"⬆️ 👨‍💼 <b>"+_("Карты дилера")+f": </b> {user['dealer_score']}")

            # print player cards
            await bot.send_sticker(message.chat.id, sticker=open(f"static/images/{message.from_user.id}_out_player.webp", 'rb').read())
            
            user = db.load_user(message.from_user.id)

            # set a keyboard
            main_menu_markup = kbd.new_game()

            # print player score
            await message.answer(f"⬆️ 👨‍💼 <b>"+_("Ваши карты")+f": </b> {user['player_score']}\n"+_("Вы победили!")+f" 🥃\n<b>"+_("Чистый выигрыш")+f"</b>: {current_win} 💴", reply_markup=main_menu_markup)

            game_controls.collect_statistics(
                message.from_user.id,
                game_result=config.GAME_WIN,
                current_win=current_win,
                is_all_in=is_all_in,
                balance=total_win,
                is_blackjack=True
            )
            
            return;

        # if player picks too many cards
        if (user['player_score'] > 21):
            # updating scrore if player has Ace in them
            for i in player_cards:
                if (i.get('value') == "Туз" and i.get('cost') == 11):
                    user['player_score']-=10
                    i['cost'] = 1
                    db.update(table='users', set='player_score = %s, player_cards = %s', where='user_id = %s', values=(user['player_score'], str(player_cards), message.from_user.id, ))

            # if player loses
            if (user['player_score'] > 21):
                
                # update player score
                total_win = user['balance']-float(user['bet'])

                # print dealer cards and score
                await bot.send_sticker(message.chat.id, sticker=open(f"static/images/{message.from_user.id}_out_dealer_open.webp", 'rb').read())
                user = db.load_user(message.from_user.id)
                await message.answer(f"⬆️ 👨‍💼 <b>"+_("Карты дилера")+f": </b> {user['dealer_score']}")

                # print player cards
                await bot.send_sticker(message.chat.id, sticker=open(f"static/images/{message.from_user.id}_out_player.webp", 'rb').read())
                user = db.load_user(message.from_user.id)
                
                # keyboard
                main_menu_markup = kbd.new_game()
                
                # print player score
                await message.answer(f"⬆️ 👨‍💼 <b>"+_("Ваши карты")+f": </b> {user['player_score']}\n"+_("Перебор! Вы проиграли")+" ❌\n"+_("Проигрыш")+f": -{float(user['bet'])}", reply_markup=main_menu_markup)

                game_controls.collect_statistics(message.from_user.id, game_result=config.GAME_LOST, is_all_in=is_all_in, balance=total_win)
                
                if total_win==0:
                    await message.answer("😔 "+_("К сожалению вы проиграли все средства\n\n<b>Но не время отчаиваться!</b> 😉\nКак только вы начнете новую игру, на вашем счету уже будут 100 монет! 🪙"))

                return;

        # print dealer hided cards and score
        await bot.send_sticker(message.chat.id, sticker=open(f"static/images/{message.from_user.id}_out_dealer_close.webp", 'rb').read())
        await message.answer(f"⬆️ 👨‍💼 <b>"+_("Карты дилера")+f": </b> "+_("Скрыто"))

        # print player cards and score
        await bot.send_sticker(message.chat.id, sticker=open(f"static/images/{message.from_user.id}_out_player.webp", 'rb').read())
        user = db.load_user(message.from_user.id)
        await message.answer(f"⬆️ 👨‍💼 <b>"+_("Ваши карты")+f": </b> {user['player_score']}", reply_markup=continue_game_controls_markup)

    # if player decides to stand
    if (message.text == _("Стоп 🛑")):
        # load player data from db
        user         = db.load_user(message.from_user.id)
        dealer_cards = list(eval(user['dealer_cards']))
        player_cards = list(eval(user['player_cards']))
        deck         = list(eval(user['deck']))
        is_all_in    = user['is_all_in']
        img_path_dealer = []
        img_path        = []

        # basic check
        if (user['is_game'] == False):
            await message.answer(_("Для начала начните новую игру"))
            return;

        # generate image for player
        for i in range(len(player_cards)):
            img_path.append(player_cards[i]['image'])
        
        game_controls.render_cards(img_path, len(player_cards), f"{message.from_user.id}_out_player.webp")
        
        # managing dealer moves
        while (user['dealer_score'] < 17):
            # randomly dealing a card for dealer
            dealer_card = random.choice(deck)
            dealer_cards.append(dealer_card)
            deck.remove(dealer_card)
            user['dealer_score'] += dealer_card.get('cost')

            db.update(table='users', set='dealer_score = %s, deck = %s, dealer_cards = %s', where='user_id = %s', values=(str(user['dealer_score']), str(deck), str(dealer_cards), message.from_user.id, ))
            
            user = db.load_user(message.from_user.id)
            dealer_cards = list(eval(user['dealer_cards']))
            deck         = list(eval(user['deck']))
            
            # generate cards paths
            img_path_dealer = []
            for i in range(len(dealer_cards)):
                img_path_dealer.append(dealer_cards[i]['image'])

            # generate image with paths
            game_controls.render_cards(img_path_dealer, len(dealer_cards), f"{message.from_user.id}_out_dealer_open.webp")

            # if dealer picks too many cards
            if (user['dealer_score'] > 21):
                # updating scrore if player has Ace in them
                for i in dealer_cards:
                    if (i.get('value') == "Туз" and i.get('cost') == 11):
                        user['dealer_score']-=10
                        i['cost'] = 1
                        db.update(table='users', set='dealer_score = %s, dealer_cards = %s', where='user_id = %s', values=(user['dealer_score'], str(dealer_cards), message.from_user.id, ))
                
                # if dealer loses, player win
                if (user['dealer_score'] > 21):
                    current_win = float(user['bet'])
                    total_win = current_win+user['balance'] # update player win

                    # print dealer cards and score
                    await bot.send_sticker(message.chat.id, sticker=open(f"static/images/{message.from_user.id}_out_dealer_open.webp", 'rb').read())
                    
                    user = db.load_user(message.from_user.id)
                    await message.answer(f"⬆️ 👽 <b>"+_("Карты дилера")+f": </b> {user['dealer_score']}")
                    
                    # print player cards and score
                    await bot.send_sticker(message.chat.id, sticker=open(f"static/images/{message.from_user.id}_out_player.webp", 'rb').read())
                    user = db.load_user(message.from_user.id)

                    # keyboard
                    main_menu_markup = kbd.new_game()
                    await message.answer(f"⬆️ 👨‍💼 <b>"+_("Ваши карты")+f": </b> {user['player_score']}\n"+_("Вы победили!")+f" 🥃\n<b>"+_("Чистый выигрыш")+f"</b>: {current_win} 💴", reply_markup=main_menu_markup)

                    game_controls.collect_statistics(message.from_user.id, game_result=config.GAME_WIN, current_win=current_win,is_all_in=is_all_in, balance=total_win)

                    return
                break
            
        user = db.load_user(message.from_user.id)            
        dealer_cards = list(eval(user['dealer_cards']))

        # generate cards image
        for i in range(len(dealer_cards)):
            img_path_dealer.append(dealer_cards[i]['image'])
        game_controls.render_cards(img_path_dealer, len(dealer_cards), f"{message.from_user.id}_out_dealer_open.webp")
        
        # player wins
        if (user['dealer_score'] < user['player_score']):
            current_win = float(user['bet'])
            # update player score
            total_win = current_win+user['balance']
            
            # print dealer cards and score
            await bot.send_sticker(message.chat.id, sticker=open(f"static/images/{message.from_user.id}_out_dealer_open.webp", 'rb').read())
            user = db.load_user(message.from_user.id)
            await message.answer(f"⬆️ 👽 <b>"+_("Карты дилера")+f": </b> {user['dealer_score']}")
            
            # print player cards and score
            await bot.send_sticker(message.chat.id, sticker=open(f"static/images/{message.from_user.id}_out_player.webp", 'rb').read())
            user = db.load_user(message.from_user.id)

            # keyboard
            main_menu_markup = kbd.new_game()

            await message.answer(f"⬆️ 👨‍💼 <b>"+_("Ваши карты")+f": </b> {user['player_score']}\n"+_("Вы победили")+f"! 🥃\n<b>"+_("Чистый выигрыш")+f"</b>: {current_win} 💴", reply_markup=main_menu_markup)

            game_controls.collect_statistics(message.from_user.id, game_result=config.GAME_WIN,current_win=current_win, is_all_in=is_all_in, balance=total_win)

        # dealer wins
        if (user['dealer_score'] > user['player_score']):
            total_win = user['balance']-float(user['bet']) # update loss

            # print dealer cards and score
            await bot.send_sticker(message.chat.id, sticker=open(f"static/images/{message.from_user.id}_out_dealer_open.webp", 'rb').read())
            user = db.load_user(message.from_user.id)
            await message.answer(f"⬆️ 👽 <b>"+_("Карты дилера")+f": </b> {user['dealer_score']}")
            
            # print player cards and score
            await bot.send_sticker(message.chat.id, sticker=open(f"static/images/{message.from_user.id}_out_player.webp", 'rb').read())
            user = db.load_user(message.from_user.id)

            # keyboard
            main_menu_markup = kbd.new_game()

            await message.answer(f"⬆️ 👨‍💼 <b>"+_("Ваши карты")+f": </b> {user['player_score']}\n"+_("Вы проиграли")+f" ❌\n"+_("Проигрыш")+f": -{float(user['bet'])}", reply_markup=main_menu_markup)

            game_controls.collect_statistics(message.from_user.id, game_result=config.GAME_LOST, is_all_in=is_all_in, balance=total_win)

            if total_win==0:
                await message.answer("😔 "+_("К сожалению вы проиграли все средства\n\n<b>Но не время отчаиваться!</b> 😉\nКак только вы начнете новую игру, на вашем счету уже будут 100 монет! 🪙"))
    
        # TIE game
        if (user['dealer_score'] == user['player_score']):
            # print dealer revealed cards
            await bot.send_sticker(message.chat.id, sticker=open(f"static/images/{message.from_user.id}_out_dealer_open.webp", 'rb').read())
            
            user = db.load_user(message.from_user.id)
            # print dealer score
            await message.answer(f"⬆️ 👽 <b>"+_("Карты дилера")+f": </b> {user['dealer_score']}")
            
            # print player cards
            await bot.send_sticker(message.chat.id, sticker=open(f"static/images/{message.from_user.id}_out_player.webp", 'rb').read())
            user = db.load_user(message.from_user.id)

            # keyboard
            main_menu_markup = kbd.new_game()

            # print player score
            await message.answer(f"⬆️ 👨‍💼 <b>"+_("Ваши карты")+f": </b> {user['player_score']}\n"+_("Ничья"), reply_markup=main_menu_markup)

            game_controls.collect_statistics(message.from_user.id, game_result=config.GAME_TIED, balance=user['balance'], is_all_in=is_all_in)

    # if player gives up
    if (message.text == _("Сдаюсь 😵")):
        # loading main variables from db
        user         = db.load_user(message.from_user.id)
        dealer_cards = list(eval(user['dealer_cards']))
        player_cards = list(eval(user['player_cards']))
        deck         = list(eval(user['deck']))
        is_all_in    = user['is_all_in']

        # basic check
        if (user['is_game'] == False):
            await message.answer(_("Для начала начните новую игру"))
            return;

        # update score
        total_win = user['balance']-float(user['bet'])
        
        # render dealer revealed cards
        game_controls.render_cards([dealer_cards[0]['image'], dealer_cards[1]['image']], 2, f"{message.from_user.id}_out_dealer_open.webp")
        
        # print dealer cards and score
        await bot.send_sticker(message.chat.id, sticker=open(f"static/images/{message.from_user.id}_out_dealer_open.webp", 'rb').read())
        user = db.load_user(message.from_user.id)
        await message.answer(f"⬆️ 👽 <b>"+_("Карты дилера")+f": </b> {user['dealer_score']}")
        
        # print player cards
        await bot.send_sticker(message.chat.id, sticker=open(f"static/images/{message.from_user.id}_out_player.webp", 'rb').read())
        user = db.load_user(message.from_user.id)

        # keyboard
        main_menu_markup = kbd.new_game()

        # print dealer score
        await message.answer(f"⬆️ 👨‍💼 <b>"+_("Ваши карты")+f": </b> {user['player_score']}\n"+_("Вы сдались")+f" :(\n"+_("Проигрыш")+f": -{float(user['bet'])}", reply_markup=main_menu_markup)
        
        # upates a lot of data in database
        game_controls.collect_statistics(message.from_user.id, game_result=config.GAME_LOST, is_all_in=is_all_in, balance=total_win)

        if total_win==0:
            await message.answer("😔 "+_("К сожалению вы проиграли все средства\n\n<b>Но не время отчаиваться!</b> 😉\nКак только вы начнете новую игру, на вашем счету уже будут 100 монет! 🪙"))
        
    # view balance
    if (message.text == _("Просмотреть баланс 💰")):
        user = db.load_user(message.from_user.id)
        await message.answer(_("💰 Баланс: ")+ str(user['balance']))