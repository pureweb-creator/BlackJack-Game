import os
from dotenv import load_dotenv

load_dotenv()

# dbconnect info
DATABASE=os.getenv("DATABASE")
HOST=os.getenv("HOST")
PG_PORT=os.getenv("PG_PORT")
API_TOKEN = os.getenv('API_TOKEN')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')

# for better perfomance
GAME_LOST = -1
GAME_WIN = 1
GAME_TIED = 0
IS_ALL_IN = True
