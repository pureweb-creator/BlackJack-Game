import logging
import asyncio
from aiogram import Bot, Dispatcher
import config
from db import DBh
from helpers.game_controls import Game_controls
from helpers.keyboards import Keyboard

# load game controls
game_controls = Game_controls()

# Configure logging
logging.basicConfig(level=logging.INFO)

# prerequisites
if not config.API_TOKEN:
    exit("No token provided")

# get event loop
loop = asyncio.get_event_loop()

# init
bot = Bot(token=config.API_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, loop=loop)

# database config
db = DBh(
    database=config.DATABASE,
    user=config.USER,
    password=config.PASSWORD,
    host=config.HOST,
    port=config.PG_PORT
)