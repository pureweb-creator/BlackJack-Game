import json
import random

from aiogram import types
from dispatcher import dp
from dispatcher import bot
from bot import db

from functions import render_image

dealer_score = 0

# keyboard
new_game_btn = types.KeyboardButton("Новая игра")
new_game_markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(new_game_btn)

# get help command
@dp.message_handler(commands=['help'])
async def info_help(message: types.Message):
    await message.answer("Связаться с разработчиком: @kallmeroma")

# get balance command
@dp.message_handler(commands=['balance'])
async def get_balance(message: types.Message):
    user = db.load_user(message.from_user.id)
    await message.answer("💰 Баланс: "+ str(user[0][2]))

# get rules command
@dp.message_handler(commands=['rules'])
async def rules(message: types.Message):
    await message.answer("""♦️ <b>Правила игры в Блэк-Джек (двадцать одно)</b> ♦️\n
Мы предоставим краткий свод правил для тех, кто никогда не играл в блэкджек.\n
Магическое число для блэкджека — 21.\nЗначения всех карт, розданных игроку, складываются, и если сумма превышает 21, игрок вылетает и мгновенно проигрывает.\n
Если игрок получает ровно 21, игрок выигрывает у дилера.\nВ противном случае для выигрыша сумма карт игрока должна быть больше суммы карт дилера.\n
Стоимости карт:
- Валет - 2 очка;\n- Дама - 3 очка;\n- Король - 4 очка;\n- Туз - 11 очков (если сумма карт больше 21, может стоить 1 очко);\nСтоимость остальных карт определяется их номиналом.""")

# start command 
@dp.message_handler(commands=['start'])
async def process_start_game(message: types.Message):
    '''bot start'''
    
    global user

    # updating deck of cards
    with open('static/deck_of_cards.json','r', encoding="utf-8") as input_f:
        deck = json.load(input_f)
    input_f.close()

    db.update(table='user', set='deck = ?', where='user_id = ?', values=(str(deck), message.from_user.id,))

    user = db.load_user(message.from_user.id)
    if (not user):
        # register user
        db.add_user(int(message.from_user.id))
        db.update(table='user', set='is_game = ?', where='user_id = ?', values=(True, message.from_user.id,))


    if user[0][2] < 1:
        user = list(user[0])
        user[2] = 100
        user = tuple([user])
        db.update(table='user', set='balance = ?, is_game = ?', where='user_id = ?', values=(100, True, message.from_user.id,))

    else: db.update(table='user', set='is_game = ?', where='user_id = ?', values=(True, message.from_user.id,))
    
    # keyboard
    game_type_markup_computer = types.KeyboardButton("Играть с компьютером 🤖")
    game_type_markup_online = types.KeyboardButton("Играть с другом 👨‍🦰 (в разработке)")
    game_type_markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(game_type_markup_computer, game_type_markup_online)
    
    await bot.send_sticker(message.from_user.id, "CAACAgIAAxkBAAEEtKFie91Ts3FZ99cztCfWqfxAqNn4FgACaQIAArrAlQUw5zOp4KLsaCQE")
    await message.answer("Выберите тип игры", reply_markup=game_type_markup)

# main game logic
@dp.message_handler(content_types=["text"])
async def process_handler(message: types.Message):
    '''button handlers'''
    if message.chat.type == "private":
        if message.text == "Новая игра":
            global user
            
            # updating deck of cards
            with open('static/deck_of_cards.json','r', encoding="utf-8") as input_f:
                deck = json.load(input_f)
            input_f.close()

            db.update(table='user', set='deck = ?', where='user_id = ?', values=(str(deck), message.from_user.id,))

            user = db.load_user(message.from_user.id)

            # update player score is he lost everything
            if user[0][2] < 1:
                user = list(user[0])
                user[2] = 100
                user = tuple([user])
                db.update(table='user', set='balance = ?, is_game = ?', where='user_id = ?', values=(100, True, message.from_user.id,))

            else: db.update(table='user', set='is_game = ?', where='user_id = ?', values=(True, message.from_user.id,))

            # keyboard
            game_type_markup_computer = types.KeyboardButton("Играть с компьютером 🤖")
            game_type_markup_online = types.KeyboardButton("Играть с другом 👨‍🦰 (в разработке)")
            game_type_markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(game_type_markup_computer, game_type_markup_online)
            await message.answer("Выберите тип игры", reply_markup=game_type_markup)

        if message.text == "Играть с компьютером 🤖":
            user = db.load_user(message.from_user.id)
            if (user[0][3] == False):
                await message.answer("Для начала начните новую игру")
                return;

            # keyboard
            balance_btn = types.KeyboardButton("💰 Баланс: "+ str(user[0][2]))
            pet_1_btn   = types.KeyboardButton("1 💲")
            pet_10_btn  = types.KeyboardButton("10 💲")
            pet_25_btn  = types.KeyboardButton("25 💲")
            pet_50_btn  = types.KeyboardButton("50 💲")
            pet_100_btn = types.KeyboardButton("100 💲")
            pet_all_in_btn = types.KeyboardButton(str(user[0][2]) + " 💲")

            sample_markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
                pet_1_btn,
                pet_10_btn,
                pet_25_btn,
                pet_50_btn,
                pet_100_btn,
                pet_all_in_btn,
                balance_btn
            )
            await message.answer("Сделайте ставку", reply_markup=sample_markup)

        if ("💲" in message.text):
            user = db.load_user(message.from_user.id)

            if (user[0][3] == False):
                await message.answer("Для начала начните новую игру")
                return;

            '''Start game'''
            global dealer_score, player_score, player_cards, dealer_cards, pet, heading_msg
            # reset all our local variables
            deck         = []
            dealer_cards = []
            player_cards = []
            player_score = 0
            dealer_score = 0

            # keyboard
            more_btn = types.KeyboardButton("Еще")
            stop_btn = types.KeyboardButton("Стоп")
            give_up_btn = types.KeyboardButton("Сдаюсь")
            game_controls_markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
                more_btn, stop_btn, give_up_btn
            )

            deck = list(eval(user[0][9]))

            pet = message.text.split()[0]
            db.update(table='user', set='pet = ?',where='user_id = ?', values=(pet, message.from_user.id,))
            user = db.load_user(message.from_user.id)
            pet = user[0][4]
        
            if (int(pet) > int(user[0][2])):
                await message.answer("На вашем балансе недостаточно средств.")
                return

            await message.answer(f"Ставка в {message.text} принята.🤑 Приятной игры!")
            heading_msg = f"<b>Ставка</b>: {pet}| <b>Баланс: </b>{user[0][2]}\n"
            
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

            db.update(table='user', set='player_score = ?, deck = ?, player_cards = ?, dealer_cards = ?, dealer_score = ?', where='user_id = ?', values=(player_score, str(deck), str(player_cards), str(dealer_cards), dealer_score, message.from_user.id,))
            user = db.load_user(message.from_user.id)

            player_score = user[0][5]

            # print
            render_image([dealer_cards[0]['image'], 'static/images/back.png'], 2, f"{message.from_user.id}_out_dealer_close.webp")
            await message.answer(heading_msg, reply_markup=game_controls_markup)
            await bot.send_sticker(message.chat.id, sticker=open(f"static/images/{message.from_user.id}_out_dealer_close.webp", 'rb').read())
            await message.answer(f"⬆️ 👽 <b>Карты дилера: </b> {dealer_cards[0]['cost']}")
            
            #print
            render_image([player_cards[0]['image'], player_cards[1]['image']], 2, f"{message.from_user.id}_out_player.webp")
            await bot.send_sticker(message.chat.id, sticker=open(f"static/images/{message.from_user.id}_out_player.webp", 'rb').read())
            await message.answer(f"⬆️ 👨‍💼 <b>Ваши карты: </b> {player_score}")

            # Player gets a blackjack  
            if (player_score == 21):
                global new_game_markup
                current_win = float(pet)*float(1.5)
                total_win = float(pet)*float(1.5)+user[0][2]
                db.update(table='user', set='player_score = ?, is_game = ?, balance = ?', where='user_id = ?', values=(player_score, False, total_win, message.from_user.id, ))
                await message.answer(f"У вас Блэк-Джек! Вы победили! 🥃\n<b>Чистый выигрыш</b>: {current_win} 💴", reply_markup=new_game_markup)

        # if player decides to go on
        if (message.text == "Еще"):

            user         = db.load_user(message.from_user.id)
            pet          = user[0][4]
            player_score = user[0][5]
            dealer_cards = list(eval(user[0][8]))
            player_cards = list(eval(user[0][7]))
            deck         = list(eval(user[0][9]))

            heading_msg = f"<b>Ставка</b>: {pet}| <b>Баланс: </b>{user[0][2]}\n"

            if (user[0][3] == False):
                await message.answer("Для начала начните новую игру")
                return;

            # randomly dealing a card for player
            player_card = random.choice(deck)
            player_cards.append(player_card)
            deck.remove(player_card)
            player_score += player_card.get('cost')

            db.update(table='user', set='player_score = ?, deck = ?, player_cards = ?', where='user_id = ?', values=(str(player_score), str(deck), str(player_cards), message.from_user.id, ))
            user = db.load_user(message.from_user.id)
            
            player_score = user[0][5]

            # generate image
            img_path = []
            for i in range(len(player_cards)):
                img_path.append(player_cards[i]['image'])
            
            render_image(img_path, len(player_cards), f"{message.from_user.id}_out_player.webp")
            render_image([dealer_cards[0]['image'], 'static/images/back.png'], 2, f"{message.from_user.id}_out_dealer_close.webp")
            render_image([dealer_cards[0]['image'], dealer_cards[1]['image']], 2, f"{message.from_user.id}_out_dealer_open.webp")

            # keyboard
            more_btn = types.KeyboardButton("Еще")
            stop_btn = types.KeyboardButton("Стоп")
            continue_game_controls_markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(more_btn, stop_btn)
            
            await message.answer(heading_msg, reply_markup=continue_game_controls_markup)

            # if player wons
            if (player_score == 21):
                current_win = float(pet)*float(1.5)
                total_win = float(pet)+user[0][2] # update win
                
                await bot.send_sticker(message.chat.id, sticker=open(f"static/images/{message.from_user.id}_out_dealer_open.webp", 'rb').read())
                await message.answer(f"⬆️ 👽 <b>Карты дилера: </b> {dealer_score}")
                
                await bot.send_sticker(message.chat.id, sticker=open(f"static/images/{message.from_user.id}_out_player.webp", 'rb').read())
                await message.answer(f"⬆️ 👨‍💼 <b>Ваши карты: </b> {player_score}\nВы победили! 🥃\n<b>Чистый выигрыш</b>: {current_win} 💴", reply_markup=new_game_markup)

                db.update(table='user', set='balance = ?, is_game = ?', where='user_id = ?', values=(total_win, False, message.from_user.id, ))

                return;

            # if player picks too many cards
            if (player_score > 21):
                # updating scrore if player has Ace in them
                for i in player_cards:
                    if (i.get('value') == "Туз" and i.get('cost') == 11):
                        player_score-=10
                        i['cost'] = 1

                        db.update(table='user', set='player_score = ?, player_cards = ?', where='user_id = ?', values=(player_score, str(player_cards), message.from_user.id, ))

                # if player loses
                if (player_score > 21):
                    total_win = user[0][2]-float(pet) # update loss
                    
                    await bot.send_sticker(message.chat.id, sticker=open(f"static/images/{message.from_user.id}_out_dealer_open.webp", 'rb').read())
                    await message.answer(f"⬆️ 👽 <b>Карты дилера: </b> {dealer_score}")
                    
                    await bot.send_sticker(message.chat.id, sticker=open(f"static/images/{message.from_user.id}_out_player.webp", 'rb').read())
                    await message.answer(f"⬆️ 👨‍💼 <b>Ваши карты: </b> {player_score}\nПеребор! Вы проиграли ❌\nПроигрыш: -{float(pet)}", reply_markup=new_game_markup)

                    db.update(table='user', set='balance = ?, is_game = ?', where='user_id = ?', values=(total_win, False, message.from_user.id, ))
                    return;
            
            await bot.send_sticker(message.chat.id, sticker=open(f"static/images/{message.from_user.id}_out_dealer_close.webp", 'rb').read())
            await message.answer(f"⬆️ 👨‍💼 <b>Карты дилера: </b> {dealer_cards[0]['cost']}")

            await bot.send_sticker(message.chat.id, sticker=open(f"static/images/{message.from_user.id}_out_player.webp", 'rb').read())
            await message.answer(f"⬆️ 👨‍💼 <b>Ваши карты: </b> {player_score}")

        # if player decides to stand
        if (message.text == "Стоп"):

            user         = db.load_user(message.from_user.id)
            pet          = user[0][4]
            player_score = user[0][5]
            dealer_score = user[0][6]
            dealer_cards = list(eval(user[0][8]))
            player_cards = list(eval(user[0][7]))
            deck         = list(eval(user[0][9]))
            img_path_dealer = []
            img_path        = []

            if (user[0][3] == False):
                await message.answer("Для начала начните новую игру")
                return;

            # generate image for player
            for i in range(len(player_cards)):
                img_path.append(player_cards[i]['image'])
            render_image(img_path, len(player_cards), f"{message.from_user.id}_out_player.webp")
            
            # managing dealer moves
            while (dealer_score < 17):
                # randomly dealing a card for dealer
                dealer_card = random.choice(deck)
                dealer_cards.append(dealer_card)
                deck.remove(dealer_card)
                dealer_score += dealer_card.get('cost')

                db.update(table='user', set='dealer_score = ?, deck = ?, dealer_cards = ?', where='user_id = ?', values=(str(dealer_score), str(deck), str(dealer_cards), message.from_user.id, ))
                
                user = db.load_user(message.from_user.id)
                dealer_cards = list(eval(user[0][8]))
                dealer_score = user[0][6]
                deck         = list(eval(user[0][9]))
                
                for i in range(len(dealer_cards)):
                    img_path_dealer.append(dealer_cards[i]['image'])
                render_image(img_path_dealer, len(dealer_cards), f"{message.from_user.id}_out_dealer_open.webp")

                # if dealer picks too many cards
                if (dealer_score > 21):
                    # updating scrore if player has Ace in them
                    for i in dealer_cards:
                        if (i.get('value') == "Туз" and i.get('cost') == 11):
                            dealer_score-=10
                            i['cost'] = 1

                            db.update(table='user', set='dealer_score = ?, dealer_cards = ?', where='user_id = ?', values=(dealer_score, str(dealer_cards), message.from_user.id, ))
                    
                    # if dealer loses, player win
                    if (dealer_score > 21):
                        current_win = float(pet)*float(1.5)
                        total_win = float(pet)+user[0][2] # update player win

                        await bot.send_sticker(message.chat.id, sticker=open(f"static/images/{message.from_user.id}_out_dealer_open.webp", 'rb').read())
                        await message.answer(f"⬆️ 👽 <b>Карты дилера: </b> {dealer_score}")
                        
                        await bot.send_sticker(message.chat.id, sticker=open(f"static/images/{message.from_user.id}_out_player.webp", 'rb').read())
                        await message.answer(f"⬆️ 👨‍💼 <b>Ваши карты: </b> {player_score}\nВы победили! 🥃\n<b>Чистый выигрыш</b>: {current_win} 💴", reply_markup=new_game_markup)

                        db.update(table='user', set='balance = ?, is_game = ?', where='user_id = ?', values=(total_win, False, message.from_user.id, ))

                        return
                    break
                
            user = db.load_user(message.from_user.id)            
            dealer_cards = list(eval(user[0][8]))
            dealer_score = user[0][6]
            player_score = user[0][5]

            for i in range(len(dealer_cards)):
                img_path_dealer.append(dealer_cards[i]['image'])
            render_image(img_path_dealer, len(dealer_cards), f"{message.from_user.id}_out_dealer_open.webp")
            
            # if dealer loses, player win
            if (dealer_score < player_score):
                current_win = float(pet)*float(1.5)
                total_win = float(pet)+user[0][2] # update player win
                
                await bot.send_sticker(message.chat.id, sticker=open(f"static/images/{message.from_user.id}_out_dealer_open.webp", 'rb').read())
                await message.answer(f"⬆️ 👽 <b>Карты дилера: </b> {dealer_score}")
                
                await bot.send_sticker(message.chat.id, sticker=open(f"static/images/{message.from_user.id}_out_player.webp", 'rb').read())
                await message.answer(f"⬆️ 👨‍💼 <b>Ваши карты: </b> {player_score}\nВы победили! 🥃\n<b>Чистый выигрыш</b>: {current_win} 💴", reply_markup=new_game_markup)

                db.update(table='user', set='balance = ?, is_game = ?', where='user_id = ?', values=(total_win, False, message.from_user.id, ))

            # if player loses, dealer win
            if (dealer_score > player_score):
                total_win = user[0][2]-float(pet) # update loss

                await bot.send_sticker(message.chat.id, sticker=open(f"static/images/{message.from_user.id}_out_dealer_open.webp", 'rb').read())
                await message.answer(f"⬆️ 👽 <b>Карты дилера: </b> {dealer_score}")
                
                await bot.send_sticker(message.chat.id, sticker=open(f"static/images/{message.from_user.id}_out_player.webp", 'rb').read())
                await message.answer(f"⬆️ 👨‍💼 <b>Ваши карты: </b> {player_score}\nВы проиграли ❌\nПроигрыш: -{float(pet)}", reply_markup=new_game_markup)

                db.update(table='user', set='balance = ?, is_game = ?', where='user_id = ?', values=(total_win, False, message.from_user.id, ))
        
            # if draw
            if (dealer_score == player_score):
                await bot.send_sticker(message.chat.id, sticker=open(f"static/images/{message.from_user.id}_out_dealer_open.webp", 'rb').read())
                await message.answer(f"⬆️ 👽 <b>Карты дилера: </b> {dealer_score}")
                
                await bot.send_sticker(message.chat.id, sticker=open(f"static/images/{message.from_user.id}_out_player.webp", 'rb').read())
                await message.answer(f"⬆️ 👨‍💼 <b>Ваши карты: </b> {player_score}\nНичья", reply_markup=new_game_markup)

        # if player gives up
        if (message.text == "Сдаюсь"):

            user         = db.load_user(message.from_user.id)
            pet          = user[0][4]
            player_score = user[0][5]
            dealer_cards = list(eval(user[0][8]))
            player_cards = list(eval(user[0][7]))
            deck         = list(eval(user[0][9]))
            img_path_dealer = []

            if (user[0][3] == False):
                await message.answer("Для начала начните новую игру")
                return;

            total_win = user[0][2]-float(pet) # update loss

            render_image([dealer_cards[0]['image'], dealer_cards[1]['image']], 2, f"{message.from_user.id}_out_dealer_open.webp")
            
            await bot.send_sticker(message.chat.id, sticker=open(f"static/images/{message.from_user.id}_out_dealer_open.webp", 'rb').read())
            await message.answer(f"⬆️ 👽 <b>Карты дилера: </b> {dealer_score}")
            
            await bot.send_sticker(message.chat.id, sticker=open(f"static/images/{message.from_user.id}_out_player.webp", 'rb').read())
            await message.answer(f"⬆️ 👨‍💼 <b>Ваши карты: </b> {player_score}\nВы сдались :(\nПроигрыш: -{float(pet)}", reply_markup=new_game_markup)

            db.update(table='user', set='balance = ?, is_game = ?', where='user_id = ?', values=(total_win, False, message.from_user.id, ))




'''
выборку из бд сделать в виде словаря тем самым избавиться от кучи переменных.
'''