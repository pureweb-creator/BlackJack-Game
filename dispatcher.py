import logging
import asyncio
from aiogram import Bot, Dispatcher
import config

# Configure logging
logging.basicConfig(level=logging.INFO)

# prerequisites
if not config.API_TOKEN:
    exit("No token provided")

# get event loop
loop = asyncio.get_event_loop()

# init
bot = Bot(token=config.API_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot,loop=loop)