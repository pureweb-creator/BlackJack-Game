## ♣️♥️ BlackJack ♦️♠️

Just a simple card game telegram bot.

####**How to launch bot in your PC**
If you decided to launch this bot in your local machine, you should necessairly obsess a **PostgreSQL** database and telegram bot token.
To get token you should create bot via [@BotFather](https://t.me/BotFather) bot. Don't loose this token.

In accordance with the above you can't go on until you create bot and **postgreSQL** database.
So, if you done with it, you can follow steps below.

**Step 1.** Clone repository via https of ssh
```git clone https://github.com/pureweb-creator/BlackJack-Game.git```
or
```git@github.com:pureweb-creator/BlackJack-Game.git```
**Step 2**
Go to ```config.py``` file and replace constants by yours.
```python
DATABASE = "dbname" # database  name
HOST = "hostname" # host namae
PORT = "port" # for example 5432
API_TOKEN = "BOT TOKEN" # telegram bot token
USER = "db_user_name" # database user name
PASSWORD = "db_user_password" # database password
```
**Step 3**
Run the following command
```python db/schema.py```
It will create basic structure and seeds default data in your database.

**Step 4**
Install dependencies required to run bot
```pip install aiogram psycopg2 Pillow python-dotenv```
If command prompt says you to install some other packages, just install it.

**Step 5**
Now you can run bot
```python bot.py``` to run the bot in you local machine.

Done!

**Technology:**
- Python 3.10
- Aiogram
- PostgreSQL

**Todo:**
- [x] English localization
- [x] Some statistics for player
- [ ] p2p game