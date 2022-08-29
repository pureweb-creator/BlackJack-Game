from aiogram import types
import gettext

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

        user_balance = int(user['balance'])
        balance_btn = types.KeyboardButton(text=self._("💰 Баланс: ")+ str(user_balance))
        
        bet_1  =  int(round(user_balance/100*1, -1)) if user_balance > 100 and int(round(user_balance/100*1, -1)) > 0 else 1
        bet_10 = int(round(user_balance/100*10, -1)) if user_balance > 100 and int(round(user_balance/100*10, -1)) > 0 else 10
        bet_25 = int(round(user_balance/100*25, -1)) if user_balance > 100 and int(round(user_balance/100*25, -1)) > 0 else 25
        bet_50 = int(round(user_balance/100*50, -1)) if user_balance > 100 and int(round(user_balance/100*50, -1)) > 0 else 50
        bet_75 = int(round(user_balance/100*75, -1)) if user_balance > 100 and int(round(user_balance/100*75, -1)) > 0 else 75

        bet_1_btn   = types.KeyboardButton(f"{bet_1} 🪙")
        bet_10_btn  = types.KeyboardButton(f"{bet_10} 🪙")
        bet_25_btn  = types.KeyboardButton(f"{bet_25} 🪙")
        bet_50_btn  = types.KeyboardButton(f"{bet_50} 🪙")
        bet_75_btn = types.KeyboardButton(f"{bet_75} 🪙")
        bet_all_in_btn = types.KeyboardButton(text=self._("Ва-банк! 🤑")+f" ({user_balance})")

        return types.ReplyKeyboardMarkup(resize_keyboard=True).add(
            bet_1_btn,
            bet_10_btn,
            bet_25_btn,
            bet_50_btn,
            bet_75_btn,
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