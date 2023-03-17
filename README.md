# ♣️♥️ BlackJack ♦️♠️

Just a simple card game telegram bot.

## **How to launch this bot in your PC**
If you decided to launch this bot in your local machine, you should necessairly posess a **PostgreSQL** database and telegram bot token.
To get token you should create bot via [@BotFather](https://t.me/BotFather) bot. Don't loose this token.

In accordance with the above you can't go on until you create bot and **postgreSQL** database.
So, if you done with it, you can follow steps below.

### Step 1
Clone this repository via https
```git clone https://github.com/pureweb-creator/BlackJack-Game.git```<br>
or ssh ```git@github.com:pureweb-creator/BlackJack-Game.git```<br>
### Step 2
Go to ```config.py``` file and replace constants by yours.<br>
```python
DATABASE = "dbname" # database  name
HOST = "hostname" # for localhost is 127.0.0.1
PORT = "port" # default for postgresql is 5432
API_TOKEN = "BOT TOKEN" # telegram bot token
DBUSER = "db_user_name" # database user name
PASSWORD = "db_user_password" # database password
```
### Step 3
Use ```db/database_dump.sql``` file to create your database and tables. Simply paste that SQL commands into your postgresql console. First command creates a  database, second creates table.<br><br>

### Step 4
Install dependencies required to run bot<br><br>
```pip install aiogram psycopg2 Pillow python-dotenv```<br><br>
If command prompt says you to install some other packages, just install it.<br>

### Step 5
Now you can run bot<br><br>
```python bot.py``` to run the bot in you local machine.<br>

If you see somehing like 
```
INFO:aiogram:Bot: 21 (Black Jack) [@blackjack_test_bot]
WARNING:aiogram:Updates were skipped successfully.
INFO:aiogram.dispatcher.dispatcher:Start polling.
```
in your console, it is regarded to success, bot works correctly.

**That's all!**

## Credits info

**Technology:**
- Python 3.10
- Aiogram
- PostgreSQL

**Todo:**
- [x] English localization
- [x] Some statistics for player
- [x] dynamic bet
- [ ] referal system

>*Check issues for more information*