import json
import random

from aiogram import types
from dispatcher import dp
from dispatcher import bot
from bot import db

from functions import render_image

# main variables
pet          = 0 # ставка
player_score = 0
dealer_score = 0
player_cards = []
dealer_cards = []
deck         = [] # колода
heading_msg  = ""

# keyboard
new_game_btn = types.KeyboardButton("Новая игра")
new_game_markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(new_game_btn)

# get help
@dp.message_handler(commands=['help'])
async def info_help(message: types.Message):
    await message.answer("Правила игры в 21 (очко)\nhttps://ru.wikipedia.org/wiki/%D0%9E%D1%87%D0%BA%D0%BE_(%D0%B8%D0%B3%D1%80%D0%B0)\nСвязь с разработчиком: @kallmeroma")

# start command
@dp.message_handler(commands=['start'])
async def process_start_game(message: types.Message):
    '''bot start'''
    
    global user
    user = db.load_user(message.from_user.id)
    if (not user):
        # register user
        db.add_user(int(message.from_user.id))
    
    # keyboard
    game_type_markup_computer = types.KeyboardButton("Играть с компьютером 🤖")
    game_type_markup_online = types.KeyboardButton("Играть с другом 👨‍🦰 (в разработке)")
    game_type_markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(game_type_markup_computer, game_type_markup_online)
    
    await message.answer("Выберите тип игры", reply_markup=game_type_markup)

# main game logic
@dp.message_handler(content_types=["text"])
async def process_handler(message: types.Message):
    '''button handlers'''
    if message.chat.type == "private":
        if message.text == "Новая игра":
            global user
            user = db.load_user(message.from_user.id)

            # keyboard
            game_type_markup_computer = types.KeyboardButton("Играть с компьютером 🤖")
            game_type_markup_online = types.KeyboardButton("Играть с другом 👨‍🦰 (в разработке)")
            game_type_markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(game_type_markup_computer, game_type_markup_online)
            await message.answer("Выберите тип игры", reply_markup=game_type_markup)

        if message.text == "Играть с компьютером 🤖":
            # keyboard
            balance_btn = types.KeyboardButton("Баланс: "+ str(user[0][2]))
            pet_1_btn   = types.KeyboardButton("1 💲")
            pet_10_btn  = types.KeyboardButton("10 💲")
            pet_25_btn  = types.KeyboardButton("25 💲")
            pet_50_btn  = types.KeyboardButton("50 💲")
            pet_100_btn = types.KeyboardButton("100 💲")

            sample_markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
                pet_1_btn,
                pet_10_btn,
                pet_25_btn,
                pet_50_btn,
                pet_100_btn,
                balance_btn
            )
            await message.answer("Сделайте ставку", reply_markup=sample_markup)

        if ("💲" in message.text):
            '''Start game'''
            global dealer_score, player_score, player_cards, dealer_cards, deck, pet, heading_msg
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

            # loading deck of cards
            with open('static/deck_of_cards.json','r', encoding="utf-8") as input_f:
                deck = json.load(input_f)
            input_f.close()

            pet = message.text.split()[0] # get pet
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

            # if both of cards are Ace for player
            if player_cards[0].get('cost') == 11 and player_cards[1].get('cost') == 11:
                player_cards[0]['cost'] = 1
                player_score -= 10

            # if both of cards are Ace for dealer
            if dealer_cards[0].get('cost') == 11 and dealer_cards[1].get('cost') == 11:
                dealer_cards[0]['cost'] = 1
                dealer_score -= 10

            render_image([dealer_cards[0]['image'], 'static/images/back.png'], 2, "out_dealer_close.webp")
            await message.answer(heading_msg, reply_markup=game_controls_markup)
            await bot.send_sticker(message.chat.id, sticker=open("static/images/out_dealer_close.webp", 'rb').read())
            await message.answer(f"⬆️ 👽 <b>Карты дилера: </b> {dealer_cards[0]['cost']}")
            
            render_image([player_cards[0]['image'], player_cards[1]['image']], 2, "out_dealer_close.webp")
            await bot.send_sticker(message.chat.id, sticker=open("static/images/out_dealer_close.webp", 'rb').read())
            await message.answer(f"⬆️ 👨‍💼 <b>Ваши карты: </b> {player_score}")

            # Player gets a blackjack  
            if (player_score == 21):
                global new_game_markup
                total_win = float(pet)*float(1.5)+user[0][2]
                db.update_user(message.from_user.id, total_win)
                await message.answer(f"У вас Блэк-Джек! Вы победили", reply_markup=new_game_markup)

        # if player decides to go on
        if (message.text == "Еще"):
            # randomly dealing a card for player
            player_card = random.choice(deck)
            player_cards.append(player_card)
            deck.remove(player_card)
            player_score += player_card.get('cost')

            # generate image
            img_path = []
            for i in range(len(player_cards)):
                img_path.append(player_cards[i]['image'])
            
            render_image(img_path, len(player_cards), "out_player.webp")
            render_image([dealer_cards[0]['image'], 'static/images/back.png'], 2, "out_dealer_close.webp")
            render_image([dealer_cards[0]['image'], dealer_cards[1]['image']], 2, "out_dealer_open.webp")

            # keyboard
            more_btn = types.KeyboardButton("Еще")
            stop_btn = types.KeyboardButton("Стоп")
            continue_game_controls_markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(more_btn, stop_btn)
            
            await message.answer(heading_msg, reply_markup=continue_game_controls_markup)

            # if player wons
            if (player_score == 21):
                total_win = float(pet)+user[0][2] # update win
                
                await bot.send_sticker(message.chat.id, sticker=open("static/images/out_dealer_open.webp", 'rb').read())
                await message.answer(f"⬆️ 👽 <b>Карты дилера: </b> {dealer_score}")
                
                await bot.send_sticker(message.chat.id, sticker=open("static/images/out_player.webp", 'rb').read())
                await message.answer(f"⬆️ 👨‍💼 <b>Ваши карты: </b> {player_score}\nВы победили!", reply_markup=new_game_markup)

                db.update_user(message.from_user.id, total_win)
                return;

            # if player picks too many cards
            if (player_score > 21):
                # updating scrore if player has Ace in them
                for i in player_cards:
                    if (i.get('value') == "Туз" and i.get('cost') == 11):
                        player_score-=10
                        i['cost'] = 1

                # if player loses
                if (player_score > 21):
                    total_win = user[0][2]-float(pet) # update loss
                    
                    await bot.send_sticker(message.chat.id, sticker=open("static/images/out_dealer_open.webp", 'rb').read())
                    await message.answer(f"⬆️ 👽 <b>Карты дилера: </b> {dealer_score}")
                    
                    await bot.send_sticker(message.chat.id, sticker=open("static/images/out_player.webp", 'rb').read())
                    await message.answer(f"⬆️ 👨‍💼 <b>Ваши карты: </b> {player_score}\nПеребор! Вы проиграли", reply_markup=new_game_markup)

                    db.update_user(message.from_user.id, total_win)
                    return;

            await bot.send_sticker(message.chat.id, sticker=open("static/images/out_dealer_close.webp", 'rb').read())
            await message.answer(f"⬆️ 👨‍💼 <b>Карты дилера: </b> {dealer_cards[0]['cost']}")

            await bot.send_sticker(message.chat.id, sticker=open("static/images/out_player.webp", 'rb').read())
            await message.answer(f"⬆️ 👨‍💼 <b>Ваши карты: </b> {player_score}")

        # if player decides to stand
        if (message.text == "Стоп"):
            
            img_path_dealer = []
            
            # managing dealer moves
            while (dealer_score < 17):
                # randomly dealing a card for dealer
                dealer_card = random.choice(deck)
                dealer_cards.append(dealer_card)
                deck.remove(dealer_card)
                dealer_score += dealer_card.get('cost')
                
                for i in range(len(dealer_cards)):
                    img_path_dealer.append(dealer_cards[i]['image'])
                render_image(img_path_dealer, len(dealer_cards), "out_dealer_open.webp")

                # if dealer picks too many cards
                if (dealer_score > 21):
                    # updating scrore if player has Ace in themif (player_score > 21):
                    for i in dealer_cards:
                        if (i.get('value') == "Туз" and i.get('cost') == 11):
                            dealer_score-=10
                            i['cost'] = 1
                    
                    # if dealer loses, player win
                    if (dealer_score > 21):
                        total_win = float(pet)+user[0][2] # update player win

                        await bot.send_sticker(message.chat.id, sticker=open("static/images/out_dealer_open.webp", 'rb').read())
                        await message.answer(f"⬆️ 👽 <b>Карты дилера: </b> {dealer_score}")
                        
                        await bot.send_sticker(message.chat.id, sticker=open("static/images/out_player.webp", 'rb').read())
                        await message.answer(f"⬆️ 👨‍💼 <b>Ваши карты: </b> {player_score}\nВы победили", reply_markup=new_game_markup)

                        db.update_user(message.from_user.id, total_win)
                        return
                    break
                
            # if dealer loses, player win
            if (dealer_score < player_score):
                total_win = float(pet)+user[0][2] # update player win
                
                await bot.send_sticker(message.chat.id, sticker=open("static/images/out_dealer_open.webp", 'rb').read())
                await message.answer(f"⬆️ 👽 <b>Карты дилера: </b> {dealer_score}")
                
                await bot.send_sticker(message.chat.id, sticker=open("static/images/out_player.webp", 'rb').read())
                await message.answer(f"⬆️ 👨‍💼 <b>Ваши карты: </b> {player_score}\nВы победили", reply_markup=new_game_markup)

                db.update_user(message.from_user.id, total_win)

            # if player loses, dealer win
            if (dealer_score > player_score):
                total_win = user[0][2]-float(pet) # update loss
                
                await bot.send_sticker(message.chat.id, sticker=open("static/images/out_dealer_open.webp", 'rb').read())
                await message.answer(f"⬆️ 👽 <b>Карты дилера: </b> {dealer_score}")
                
                await bot.send_sticker(message.chat.id, sticker=open("static/images/out_player.webp", 'rb').read())
                await message.answer(f"⬆️ 👨‍💼 <b>Ваши карты: </b> {player_score}\nВы проиграли", reply_markup=new_game_markup)

                db.update_user(message.from_user.id, total_win)

        # if player gives up
        if (message.text == "Сдаюсь"):
            total_win = user[0][2]-float(pet) # update loss

            render_image([dealer_cards[0]['image'], dealer_cards[1]['image']], 2, "out_dealer_open.webp")
            
            await bot.send_sticker(message.chat.id, sticker=open("static/images/out_dealer_open.webp", 'rb').read())
            await message.answer(f"⬆️ 👽 <b>Карты дилера: </b> {dealer_score}")
            
            await bot.send_sticker(message.chat.id, sticker=open("static/images/out_player.webp", 'rb').read())
            await message.answer(f"⬆️ 👨‍💼 <b>Ваши карты: </b> {player_score}\nВы сдались :(", reply_markup=new_game_markup)

            db.update_user(message.from_user.id, total_win)