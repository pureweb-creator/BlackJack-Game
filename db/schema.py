import sys
import path
import psycopg2

dir = path.Path(__file__).abspath()
sys.path.append(dir.parent.parent)

import config

#establishing the connection
conn = psycopg2.connect(
    database=config.DATABASE,
    user=config.USER,
    password=config.PASSWORD,
    host=config.HOST,
    port=config.PG_PORT
   )
conn.autocommit = True

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Preparing query to create a database
sql = """CREATE TABLE users (id serial PRIMARY KEY, user_id integer, balance integer DEFAULT 100, is_game boolean, bet integer, player_score integer, dealer_score integer, player_cards varchar, dealer_cards varchar, deck varchar DEFAULT '[{"suit":"черви","value":2,"image":"static/images/2_of_hearts.png","cost":2},{"suit":"черви","value":3,"image":"static/images/3_of_hearts.png","cost":3},{"suit":"черви","value":4,"image":"static/images/4_of_hearts.png","cost":4},{"suit":"черви","value":5,"image":"static/images/5_of_hearts.png","cost":5},{"suit":"черви","value":6,"image":"static/images/6_of_hearts.png","cost":6},{"suit":"черви","value":7,"image":"static/images/7_of_hearts.png","cost":7},{"suit":"черви","value":8,"image":"static/images/8_of_hearts.png","cost":8},{"suit":"черви","value":9,"image":"static/images/9_of_hearts.png","cost":9},{"suit":"черви","value":10,"image":"static/images/10_of_hearts.png","cost":10},{"suit":"черви","value":"Валет","image":"static/images/jack_of_hearts.png","cost":2},{"suit":"черви","value":"Королева","image":"static/images/queen_of_hearts.png","cost":3},{"suit":"черви","value":"Король","image":"static/images/king_of_hearts.png","cost":4},{"suit":"черви","value":"Туз","image":"static/images/ace_of_hearts.png","cost":11},{"suit":"бубны","value":2,"image":"static/images/2_of_diamonds.png","cost":2},{"suit":"бубны","value":3,"image":"static/images/3_of_diamonds.png","cost":3},{"suit":"бубны","value":4,"image":"static/images/4_of_diamonds.png","cost":4},{"suit":"бубны","value":5,"image":"static/images/5_of_diamonds.png","cost":5},{"suit":"бубны","value":6,"image":"static/images/6_of_diamonds.png","cost":6},{"suit":"бубны","value":7,"image":"static/images/7_of_diamonds.png","cost":7},{"suit":"бубны","value":8,"image":"static/images/8_of_diamonds.png","cost":8},{"suit":"бубны","value":9,"image":"static/images/9_of_diamonds.png","cost":9},{"suit":"бубны","value":10,"image":"static/images/10_of_diamonds.png","cost":10},{"suit":"бубны","value":"Валет","image":"static/images/jack_of_diamonds.png","cost":2},{"suit":"бубны","value":"Королева","image":"static/images/queen_of_diamonds.png","cost":3},{"suit":"бубны","value":"Король","image":"static/images/king_of_diamonds.png","cost":4},{"suit":"бубны","value":"Туз","image":"static/images/ace_of_diamonds.png","cost":11},{"suit":"трефы","value":2,"image":"static/images/2_of_clubs.png","cost":2},{"suit":"трефы","value":3,"image":"static/images/3_of_clubs.png","cost":3},{"suit":"трефы","value":4,"image":"static/images/4_of_clubs.png","cost":4},{"suit":"трефы","value":5,"image":"static/images/5_of_clubs.png","cost":5},{"suit":"трефы","value":6,"image":"static/images/6_of_clubs.png","cost":6},{"suit":"трефы","value":7,"image":"static/images/7_of_clubs.png","cost":7},{"suit":"трефы","value":8,"image":"static/images/8_of_clubs.png","cost":8},{"suit":"трефы","value":9,"image":"static/images/9_of_clubs.png","cost":9},{"suit":"трефы","value":10,"image":"static/images/10_of_clubs.png","cost":10},{"suit":"трефы","value":"Валет","image":"static/images/jack_of_clubs.png","cost":2},{"suit":"трефы","value":"Королева","image":"static/images/queen_of_clubs.png","cost":3},{"suit":"трефы","value":"Король","image":"static/images/king_of_clubs.png","cost":4},{"suit":"трефы","value":"Туз","image":"static/images/ace_of_clubs.png","cost":11},{"suit":"пики","value":2,"image":"static/images/2_of_spades.png","cost":2},{"suit":"пики","value":3,"image":"static/images/3_of_spades.png","cost":3},{"suit":"пики","value":4,"image":"static/images/4_of_spades.png","cost":4},{"suit":"пики","value":5,"image":"static/images/5_of_spades.png","cost":5},{"suit":"пики","value":6,"image":"static/images/6_of_spades.png","cost":6},{"suit":"пики","value":7,"image":"static/images/7_of_spades.png","cost":7},{"suit":"пики","value":8,"image":"static/images/8_of_spades.png","cost":8},{"suit":"пики","value":9,"image":"static/images/9_of_spades.png","cost":9},{"suit":"пики","value":10,"image":"static/images/10_of_spades.png","cost":10},{"suit":"пики","value":"Валет","image":"static/images/jack_of_spades.png","cost":2},{"suit":"пики","value":"Королева","image":"static/images/queen_of_spades.png","cost":3},{"suit":"пики","value":"Король","image":"static/images/king_of_spades.png","cost":4},{"suit":"пики","value":"Туз","image":"static/images/ace_of_spades.png","cost":11}]', user_name varchar(20), user_lastname varchar(20), lang varchar(2) DEFAULT 'ru', games_played integer DEFAULT 0, games_won integer DEFAULT 0, games_lost INTEGER default 0, games_tied integer DEFAULT 0);"""

#Creating a database
cursor.execute(sql)
print(cursor.fetchall())
print("Database created successfully")

#Closing the connection
conn.close()