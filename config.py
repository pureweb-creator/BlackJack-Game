import os
from dotenv import load_dotenv

load_dotenv()

DATABASE=os.getenv("DATABASE")
HOST=os.getenv("HOST")
PG_PORT=os.getenv("PG_PORT")
API_TOKEN = os.getenv('API_TOKEN')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
