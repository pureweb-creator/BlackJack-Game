## ♣️♥️ BlackJack ♦️♠️

Just a simple card game telegram bot.

####**How to launch bot in your PC**
If you decided to launch this bot in your local machine, you should necessairly obsess a **PostgreSQL** database and telegram bot token.
To get token you should create bot via [@BotFather](https://t.me/BotFather) bot. Don't loose this token.

In accordance with the above you can't go on until you create bot and **postgreSQL** database.
So, if you done with it, you can follow steps below.

**Step 1.** Clone repository via https using ssh<br>
```git clone https://github.com/pureweb-creator/BlackJack-Game.git```<br>
or<br>
```git@github.com:pureweb-creator/BlackJack-Game.git```<br>
**Step 2**<br>
Go to ```config.py``` file and replace constants by yours.<br>
```python
DATABASE = "dbname" # database  name
HOST = "hostname" # host namae
PORT = "port" # for example 5432
API_TOKEN = "BOT TOKEN" # telegram bot token
USER = "db_user_name" # database user name
PASSWORD = "db_user_password" # database password
```
**Step 3**<br>
Run the following command<br>
```python db/schema.py```<br>
It will create basic structure and seeds default data in your database.<br.>

**Step 4**<br>
Install dependencies required to run bot<br>
```pip install aiogram psycopg2 Pillow python-dotenv```<br>
If command prompt says you to install some other packages, just install it.<br>

**Step 5**<br>
Now you can run bot<br>
```python bot.py``` to run the bot in you local machine.<br>

Done!

**Technology:**
- Python 3.10
- Aiogram
- PostgreSQL

**Todo:**
- [x] English localization
- [x] Some statistics for player
- [ ] p2p game