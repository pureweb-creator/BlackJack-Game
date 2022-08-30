import gettext
from config import GAME_LOST, GAME_TIED, GAME_WIN, IS_ALL_IN
from db import DBh
from PIL import Image
from aiogram import types
from dispatcher import config
from datetime import datetime, timedelta

class Game_controls(DBh):
    '''Helper functions'''
    def __init__(self):
        super().__init__(database=config.DATABASE, user=config.USER, password=config.PASSWORD, host=config.HOST, port=config.PG_PORT)
        
    def render_cards(self, img_path, img_name):
        '''Rendering an image with gaming table and cards'''
        img_list = []
        img_count = len(img_path)

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

    def collect_statistics(self, user_id, game_result, balance, current_win=None, is_all_in=None, is_blackjack=False): # default values could be None type cuz tied game result has no whether win or all-in param
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

        if (games_played == 500):
            user['balance'] += 1000000
            super().update(
                table='users',
                set='balance = %s',
                where='user_id = %s',
                values=(user['balance'], user_id))

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
        
        msg = "📈 <b>"+_("Ваша статистика")+"</b>" \
        +"\n\n<b>"+_("Имя")+f": {user_name}</b>\n" \
        +"🎲 "+_("Игр сыграно")+f": <b>{stat['games_played']}</b>\n" \
        +"✅ "+_("Игр выиграно")+f": <b>{stat['games_won']} ({percentage['gamesWon']}%)</b>\n" \
        +"🏆 "+_("Блэк-Джек")+f": <b>{stat['blackjack_count']} ({percentage['BlackJackCount']}%)</b>\n" \
        +"❌ "+_("Игр проиграно")+f": <b>{stat['games_lost']} ({percentage['gamesLost']}%)</b>\n" \
        +"😐 "+_("Игр вничью")+f": <b>{stat['games_tied']} ({percentage['gamesTied']}%)</b>\n\n" \
        +"⏩ "+_("Максимальный выигрыш")+f": <b>{stat['max_win']}</b>\n" \
        +"⏪ "+_("Максимальный проигрыш")+f": <b>{stat['max_loss']}</b>\n\n" \
        +"🤑 "+_("Пошли ва-банк (раз)")+f": <b>{stat['all_in_games_count']}</b>\n" \
        +_("Из них: ")+"\n" \
        +"✅ "+_("Выиграли")+f": <b>{stat['all_in_win']} ({percentage['AllInWin']}%)</b>\n" \
        +"❌ "+_("Проиграли")+f": <b>{stat['all_in_loss']} ({percentage['AllInLoss']}%)</b>\n" \
        +"😐 "+_("Вничью")+f": <b>{stat['all_in_tie']} ({percentage['AllInTie']}%)</b>\n\n" \
        +"⏰ "+_("Последний раз играли")+f": <b>{stat['last_played'].strftime('%m/%d/%Y, %H:%M')}</b>\n" \
        
        btn = types.InlineKeyboardButton(_('🆑 Сбросить статистику'), callback_data="confirmation")
        markup = types.InlineKeyboardMarkup().add(btn)

        return msg, markup