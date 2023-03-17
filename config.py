import os
from dotenv import load_dotenv

load_dotenv()

# dbconnect info
DATABASE    = os.getenv("DATABASE")
HOST        = os.getenv("HOST")
PG_PORT     = os.getenv("PG_PORT")
API_TOKEN   = os.getenv('API_TOKEN')
USER        = os.getenv('DBUSER')
PASSWORD    = os.getenv('PASSWORD')
DEV_CONTACT = os.getenv('DEVELOPER_CONTACT')
DBUSER = os.getenv('DBUSER')

# for better perfomance
GAME_LOST = -1
GAME_WIN  = 1
GAME_TIED = 0
IS_ALL_IN = True

STICKERS = [
    "CAACAgIAAxkBAAEFBxxip0f_tsUwKfb-TloKSEvz7GdiiQACORgAAqIyQEkGKbj_3PIXZSQE",
    "CAACAgIAAxkBAAEFBx1ip0f_KFv1IPGIb6F-1GagvezzkgAChwIAAladvQpC7XQrQFfQkCQE",
    "CAACAgIAAxkBAAEFBx5ip0f_LTUelEhM06_AjujYfQxR6gAC5QgAAgi3GQLR-yMPZfVRlCQE",
    "CAACAgIAAxkBAAEFBx9ip0f_TtZ25SGVQuO4QQwj3d2DYQACpAgAAgi3GQKcfY4krdlvRyQE",
    "CAACAgIAAxkBAAEFByBip0f_uqU8AlAacCuk9qQKkvjydQAC8QgAAgi3GQL77_YW2hgg3iQE",
    "CAACAgIAAxkBAAEFByFip0f_3NAgait_SwNsg9Y4mrFyVAACdQIAArrAlQUHDPNSndIC4SQE",
    "CAACAgIAAxkBAAEFByJip0f_9QsugPwBBTHYAn6J2S7oqwACZQIAArrAlQUmE2IOvXXA7SQE",
    "CAACAgIAAxkBAAEFByNip0f_NYlQD6qg1D_f9AO6-DQrYwACaQIAArrAlQUw5zOp4KLsaCQE",
    "CAACAgIAAxkBAAEFByRip0f_cqGZTkD1dhZgNDuH4HFO0AACbwIAArrAlQUEI4DGos7M-CQE",
    "CAACAgIAAxkBAAEFByVip0f_g13Rsr9v68X__5z1XRBE9AACVgIAArrAlQUVofROZcftZCQE",
    "CAACAgIAAxkBAAEFByZip0f_mhrNletQv3oHFol17CqbNgACTQIAArrAlQURMHbVNAnBJiQE"
]
