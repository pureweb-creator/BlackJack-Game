import sqlite3

class DBh:
    def __init__(self, database):
        '''Connecting to DB and saving connection cursor'''
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def load_user(self, user_id):
        '''load user if exists'''
        with self.connection:
            return self.cursor.execute('SELECT * FROM `user` WHERE `user_id` = ?', (user_id,)).fetchall()

    def add_user(self, user_id):
        '''register user'''
        with self.connection:
            return self.cursor.execute('INSERT INTO `user` (`user_id`) VALUES (?)', (user_id,))

    def update_user(self, user_id, balance):
        '''update user balance'''
        with self.connection:
            return self.cursor.execute('UPDATE `user` SET `balance` = ? WHERE `user_id` = ?', (balance, user_id,))

    def is_game(self, user_id, is_game):
        '''stop or start game'''
        with self.connection:
            return self.cursor.execute('UPDATE `user` SET `is_game` = ? WHERE `user_id` = ?', (is_game, user_id,))


    def close(self):
        '''Close connection with DB'''
        self.connection.close()