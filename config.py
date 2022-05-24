import os
from dotenv import load_dotenv

load_dotenv()

DATABASE=os.getenv("DATABASE")
HOST=os.getenv("HOST")
PORT="5432"
API_TOKEN = os.getenv('API_TOKEN')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
