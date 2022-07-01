from aiogram import executor
from dispatcher import dp
from dispatcher import config
import handlers

from db import DBh
db = DBh(
    database=config.DATABASE,
    user=config.USER,
    password=config.PASSWORD,
    host=config.HOST,
    port=config.PG_PORT
)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)