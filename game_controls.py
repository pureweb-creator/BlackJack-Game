import gettext
from db import DBh
from PIL import Image
from aiogram import types

class Game_controls(DBh):
    '''Useful functions'''
    def __init__(self):
        super().__init__("db.db")
        
    def render_cards(self, img_path, img_count, img_name):
        '''Rendering an image with gaming table and cards'''
        img_list = []

        # create image list
        for i in range(img_count):
            current_image = Image.open(img_path[i], 'r')
            current_image = current_image.resize((70,103),Image.ANTIALIAS)
            img_list.append(current_image)
        
        img_w, img_h = (70, 103)

        background  = Image.open('static/images/bg.png')
        bg_w, bg_h  = background.size
        offset_list = []
        offset_left = 1

        # create offsets
        for i in range(1,img_count+1):
            if (i==1): offset_list.append((15, (bg_h - img_h) // 2))
            if (i>=2): offset_list.append(((offset_left*i + img_w//4*(i-1)+10 ), (bg_h - img_h) // 2))

        # paste image cards into background table with offsets
        for i in range(len(offset_list)):
            background.paste(img_list[i], offset_list[i])

        background.save(f'static/images/{img_name}', format='webp')

    def get_locale(self, lang):
        '''load language'''
        if (lang == 'en'):
            en = gettext.translation('blackjack', localedir='locales', languages=['en'])
            en.install()
            return en.gettext

        if (lang == 'ru'):
            gettext.bindtextdomain('blackjack', 'localization/')
            gettext.textdomain('blackjack')
            return gettext.gettext

    def collect_statistics(self, user_id, is_played=False, is_won=False, is_lost=False, is_tied=False):
        '''collect some statistics for player'''
        user = super().load_statistics(user_id)
        games_won = user['games_won']
        games_played = user['games_played']
        games_tied = user['games_tied']
        games_lost = user['games_lost']

        if (is_played != False):
            games_played+=1

        if (is_won != False):
            games_won+=1
            super().update('user', 'games_won = ?, games_played = ?', 'user_id = ?', (games_won, games_played, user_id))
        
        if (is_lost != False):
            games_lost+=1
            super().update('user', 'games_lost = ?, games_played = ?', 'user_id = ?', (games_lost, games_played, user_id))
        
        if (is_tied != False):
            games_tied+=1
            super().update('user', 'games_tied = ?, games_played = ?', 'user_id = ?', (games_tied, games_played, user_id))

    def get_statistics(self, user_id):
        '''get statistics'''
        return super().load_statistics(user_id)

class Keyboard:
    '''Set of keyboards'''
    def __init__(self, lang):
        '''get current user language'''
        self.lang = lang

        if (self.lang == 'en'):
            en = gettext.translation('blackjack', localedir='locales', languages=['en'])
            en.install()
            self._ = en.gettext

        if (self.lang == 'ru'):
            gettext.bindtextdomain('blackjack', 'localization/')
            gettext.textdomain('blackjack')
            self._ = gettext.gettext

    def new_game(self):
        '''keyboard buttons for new game command'''
        main_menu_new_game_btn = types.KeyboardButton(text=self._("Начать новую игру 🎮"))
        main_menu_balance_btn = types.KeyboardButton(text=self._("Просмотреть баланс 💰"))
        return types.ReplyKeyboardMarkup(resize_keyboard=True).add(main_menu_new_game_btn, main_menu_balance_btn)

    def game_type(self):
        '''keyboard buttons for game type command'''
        game_type_markup_computer = types.KeyboardButton(text=self._("Играть с компьютером 🧠"))
        game_type_markup_online = types.KeyboardButton(text=self._("Играть с другом 👨‍🦰 (в разработке </>)"))
        return types.ReplyKeyboardMarkup(resize_keyboard=True).add(game_type_markup_computer, game_type_markup_online)

    def bet(self, user):
        '''keyboard buttons for "choose bet" command'''
        
        balance_btn = types.KeyboardButton(text=self._("💰 Баланс: ")+ str(user['balance']))
        bet_1_btn   = types.KeyboardButton("1 🪙")
        bet_10_btn  = types.KeyboardButton("10 🪙")
        bet_25_btn  = types.KeyboardButton("25 🪙")
        bet_50_btn  = types.KeyboardButton("50 🪙")
        bet_100_btn = types.KeyboardButton("100 🪙")
        bet_all_in_btn = types.KeyboardButton(text=self._("Ва-банк! 🤑")+f" ({user['balance']})")

        return types.ReplyKeyboardMarkup(resize_keyboard=True).add(
            bet_1_btn,
            bet_10_btn,
            bet_25_btn,
            bet_50_btn,
            bet_100_btn,
            bet_all_in_btn,
            balance_btn
        )

    def game_nav_1(self):
        '''keyboard buttons navigation menu during game'''

        more_btn = types.KeyboardButton(text=self._("Еще 🟢"))
        stop_btn = types.KeyboardButton(text=self._("Стоп 🛑"))
        give_up_btn = types.KeyboardButton(text=self._("Сдаюсь 😵"))

        return types.ReplyKeyboardMarkup(resize_keyboard=True).add(
            more_btn, stop_btn, give_up_btn
        )

    def game_nav_2(self):
        '''keyboard buttons navigation menu during game'''

        more_btn = types.KeyboardButton(text=self._("Еще 🟢"))
        stop_btn = types.KeyboardButton(text=self._("Стоп 🛑"))
        return types.ReplyKeyboardMarkup(resize_keyboard=True).add(more_btn, stop_btn)   