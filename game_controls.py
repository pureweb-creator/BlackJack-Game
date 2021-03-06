import gettext
from config import GAME_LOST, GAME_TIED, GAME_WIN, IS_ALL_IN
from db import DBh
from PIL import Image
from aiogram import types
from dispatcher import config
from datetime import datetime, timedelta

class Game_controls(DBh):
    '''Useful functions'''
    def __init__(self):
        super().__init__(database=config.DATABASE, user=config.USER, password=config.PASSWORD, host=config.HOST, port=config.PG_PORT)
        
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
        if (lang == 'ru'):
            gettext.bindtextdomain('blackjack', 'localization/')
            gettext.textdomain('blackjack')
            return gettext.gettext
        else:
            lang = gettext.translation('blackjack', localedir='locales', languages=[lang])
            lang.install()
            return lang.gettext

    def collect_statistics(self, user_id, game_result, balance, current_win=None, is_all_in=None, is_blackjack=False): # default values could be None type cuz tied game result has not win or all-in param
        '''Collect statistics'''
        user = super().load_user(user_id)

        # Getting the current date and time
        dt = datetime.utcnow()+timedelta(hours=3)

        # increment all games count
        games_played = user['games_played']
        games_played += 1

        # updates common info 
        super().update(
            table='users',
            set='player_score = %s, is_game = %s, last_played = %s, balance = %s, games_played = %s',
            where='user_id = %s',
            values=(user['player_score'], False, dt, balance, games_played, user_id )
        )

        # updates specific info
        if (is_all_in == IS_ALL_IN):
            all_in_games_count = user['all_in_games_count']
            all_in_games_count += 1
            super().update(table="users", set="all_in_games_count = %s", where="user_id = %s", values=(all_in_games_count, user_id, ))

        if (game_result == GAME_WIN):
            games_won = user['games_won']
            games_won += 1
            max_win = user['max_win']

            super().update(table='users', set='games_won = %s', where='user_id = %s', values=(games_won, user_id, ))

            if (is_blackjack == True):
                blackjack = user['blackjack_count'];
                blackjack += 1
                super().update(table='users', set='blackjack_count = %s', where="user_id = %s", values=(blackjack, user_id, ))

            if (current_win > max_win):
                max_win = current_win
                super().update(table='users', set='max_win = %s', where='user_id = %s', values=(max_win, user_id, ))

            if (is_all_in == IS_ALL_IN):
                all_in_win = user['all_in_win']
                all_in_win += 1
                super().update(table="users",set="all_in_win = %s", where="user_id = %s", values=(all_in_win, user_id, ))
        
        if (game_result == GAME_LOST):
            games_lost = user['games_lost']
            games_lost += 1
            max_loss = user['max_loss']

            super().update(table='users', set='games_lost = %s', where='user_id = %s', values=(games_lost, user_id ))

            if (user['bet'] > max_loss):
                max_loss = user['bet']
                super().update(table='users', set='max_loss = %s', where='user_id = %s', values=(max_loss, user_id, ))

            if (is_all_in == IS_ALL_IN):
                all_in_loss = user['all_in_loss']
                all_in_loss += 1
                super().update(table="users",set="all_in_loss = %s", where="user_id = %s", values=(all_in_loss, user_id, ))

        if (game_result == GAME_TIED):
            games_tied = user['games_tied']
            games_tied+=1
            super().update(table="users",set="games_tied = %s", where="user_id = %s", values=(games_tied, user_id, ))

            if (is_all_in == IS_ALL_IN):
                all_in_tie = user['all_in_tie']
                all_in_tie += 1
                super().update(table="users",set="all_in_tie = %s", where="user_id = %s", values=(all_in_tie, user_id, ))

    def get_statistics(self, user_id):
        '''get statistics'''
        return super().load_statistics(user_id)

    async def print_statistics(self, user_id, user_name):
        '''print user statistics'''

        # get current user locale
        user = super().load_user(user_id)
        _ = self.get_locale(user['lang'])
        
        stat = super().load_statistics(user_id)

        percentage = {
            "gamesWon": round(stat['games_won']/stat['games_played']*100 if stat['games_played'] > 0 else 0, 2),
            "gamesLost": round(stat['games_lost']/stat['games_played']*100 if stat['games_played'] > 0 else 0, 2),
            "gamesTied": round(stat['games_tied']/stat['games_played']*100 if stat['games_played'] > 0 else 0, 2),
            "AllInWin": round(stat['all_in_win']/stat['all_in_games_count']*100 if stat['all_in_games_count'] > 0 else 0, 2),
            "AllInLoss": round(stat['all_in_loss']/stat['all_in_games_count']*100 if stat['all_in_games_count'] > 0 else 0, 2),
            "AllInTie": round(stat['all_in_tie']/stat['all_in_games_count']*100 if stat['all_in_games_count'] > 0 else 0, 2),
            "BlackJackCount": round(stat['blackjack_count']/stat['games_won']*100 if stat['games_won'] > 0 else 0, 2)
        }
        
        msg = "???? <b>"+_("???????? ????????????????????")+"</b>" \
        +"\n\n<b>"+_("??????")+f": {user_name}</b>\n" \
        +"???? "+_("?????? ??????????????")+f": <b>{stat['games_played']}</b>\n" \
        +"??? "+_("?????? ????????????????")+f": <b>{stat['games_won']} ({percentage['gamesWon']}%)</b>\n" \
        +"???? "+_("????????-????????")+f": <b>{stat['blackjack_count']} ({percentage['BlackJackCount']}%)</b>\n" \
        +"??? "+_("?????? ??????????????????")+f": <b>{stat['games_lost']} ({percentage['gamesLost']}%)</b>\n" \
        +"???? "+_("?????? ????????????")+f": <b>{stat['games_tied']} ({percentage['gamesTied']}%)</b>\n\n" \
        +"??? "+_("???????????????????????? ??????????????")+f": <b>{stat['max_win']}</b>\n" \
        +"??? "+_("???????????????????????? ????????????????")+f": <b>{stat['max_loss']}</b>\n\n" \
        +"???? "+_("?????????? ????-???????? (??????)")+f": <b>{stat['all_in_games_count']}</b>\n" \
        +_("???? ??????: ")+"\n" \
        +"??? "+_("????????????????")+f": <b>{stat['all_in_win']} ({percentage['AllInWin']}%)</b>\n" \
        +"??? "+_("??????????????????")+f": <b>{stat['all_in_loss']} ({percentage['AllInLoss']}%)</b>\n" \
        +"???? "+_("????????????")+f": <b>{stat['all_in_tie']} ({percentage['AllInTie']}%)</b>\n\n" \
        +"??? "+_("?????????????????? ?????? ????????????")+f": <b>{stat['last_played'].strftime('%m/%d/%Y, %H:%M')}</b>\n" \
        
        btn = types.InlineKeyboardButton(_('???? ???????????????? ????????????????????'), callback_data="confirmation")
        markup = types.InlineKeyboardMarkup().add(btn)

        return msg, markup

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
        main_menu_new_game_btn = types.KeyboardButton(text=self._("???????????? ?????????? ???????? ????"))
        main_menu_balance_btn = types.KeyboardButton(text=self._("?????????????????????? ???????????? ????"))
        return types.ReplyKeyboardMarkup(resize_keyboard=True).add(main_menu_new_game_btn, main_menu_balance_btn)

    def game_type(self):
        '''keyboard buttons for game type command'''
        game_type_markup_computer = types.KeyboardButton(text=self._("???????????? ?? ?????????????????????? ????"))
        game_type_markup_online = types.KeyboardButton(text=self._("???????????? ?? ???????????? ??????????? (?? ???????????????????? </>)"))
        return types.ReplyKeyboardMarkup(resize_keyboard=True).add(game_type_markup_computer, game_type_markup_online)

    def bet(self, user):
        '''keyboard buttons for "choose bet" command'''
        
        balance_btn = types.KeyboardButton(text=self._("???? ????????????: ")+ str(user['balance']))
        bet_1_btn   = types.KeyboardButton("1 ????")
        bet_10_btn  = types.KeyboardButton("10 ????")
        bet_25_btn  = types.KeyboardButton("25 ????")
        bet_50_btn  = types.KeyboardButton("50 ????")
        bet_100_btn = types.KeyboardButton("100 ????")
        bet_all_in_btn = types.KeyboardButton(text=self._("????-????????! ????")+f" ({user['balance']})")

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

        more_btn = types.KeyboardButton(text=self._("?????? ????"))
        stop_btn = types.KeyboardButton(text=self._("???????? ????"))
        give_up_btn = types.KeyboardButton(text=self._("???????????? ????"))

        return types.ReplyKeyboardMarkup(resize_keyboard=True).add(
            more_btn, stop_btn, give_up_btn
        )

    def game_nav_2(self):
        '''keyboard buttons navigation menu during game'''

        more_btn = types.KeyboardButton(text=self._("?????? ????"))
        stop_btn = types.KeyboardButton(text=self._("???????? ????"))
        return types.ReplyKeyboardMarkup(resize_keyboard=True).add(more_btn, stop_btn)   