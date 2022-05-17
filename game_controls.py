import gettext
from PIL import Image
from aiogram import types

class Game_controls:
    def render_cards(self, img_path, img_count, img_name):
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

        # create image with offsets
        for i in range(len(offset_list)):
            background.paste(img_list[i], offset_list[i])

        background.save(f'static/images/{img_name}', format='webp')

    def get_locale(self, lang):
        if (lang == 'en'):
            en = gettext.translation('blackjack', localedir='locales', languages=['en'])
            en.install()
            return en.gettext

        if (lang == 'ru'):
            gettext.bindtextdomain('blackjack', 'localization/')
            gettext.textdomain('blackjack')
            return gettext.gettext

class Keyboard:
    def __init__(self, lang):
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
        main_menu_new_game_btn = types.KeyboardButton(text=self._("Начать новую игру 🎮"))
        main_menu_balance_btn = types.KeyboardButton(text=self._("Просмотреть баланс 💰"))
        return types.ReplyKeyboardMarkup(resize_keyboard=True).add(main_menu_new_game_btn, main_menu_balance_btn)

    def game_type(self):
        game_type_markup_computer = types.KeyboardButton(text=self._("Играть с компьютером 🧠"))
        game_type_markup_online = types.KeyboardButton(text=self._("Играть с другом 👨‍🦰 (в разработке </>)"))
        return types.ReplyKeyboardMarkup(resize_keyboard=True).add(game_type_markup_computer, game_type_markup_online)

    def pet(self, user):
        balance_btn = types.KeyboardButton(text=self._("💰 Баланс: ")+ str(user['balance']))
        pet_1_btn   = types.KeyboardButton("1 🪙")
        pet_10_btn  = types.KeyboardButton("10 🪙")
        pet_25_btn  = types.KeyboardButton("25 🪙")
        pet_50_btn  = types.KeyboardButton("50 🪙")
        pet_100_btn = types.KeyboardButton("100 🪙")
        pet_all_in_btn = types.KeyboardButton(text=self._("Ва-банк! 🤑")+f" ({user['balance']})")

        return types.ReplyKeyboardMarkup(resize_keyboard=True).add(
            pet_1_btn,
            pet_10_btn,
            pet_25_btn,
            pet_50_btn,
            pet_100_btn,
            pet_all_in_btn,
            balance_btn
        )

    def game_nav_1(self):
        more_btn = types.KeyboardButton(text=self._("Еще 🟢"))
        stop_btn = types.KeyboardButton(text=self._("Стоп 🛑"))
        give_up_btn = types.KeyboardButton(text=self._("Сдаюсь 😵"))

        return types.ReplyKeyboardMarkup(resize_keyboard=True).add(
            more_btn, stop_btn, give_up_btn
        )

    def game_nav_2(self):
        more_btn = types.KeyboardButton(text=self._("Еще 🟢"))
        stop_btn = types.KeyboardButton(text=self._("Стоп 🛑"))
        return types.ReplyKeyboardMarkup(resize_keyboard=True).add(more_btn, stop_btn)   