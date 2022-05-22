import psycopg2

class DBh:
    def __init__(self, database, user, password, host, port):
        """Connecting to DB and saving connection cursor"""

        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        
        self.connection = psycopg2.connect(database=self.database, user=self.user, password=self.password, host='ec2-63-35-156-160.eu-west-1.compute.amazonaws.com', port=self.port)
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()
        
    def load_user(self, user_id):
        """load user if exists"""
        with self.connection:
            user = self.cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,)).fetchall()
            if user:
                user = [{k: item[k] for k in item.keys()} for item in user]
                return user[0]
            return False

    def load_statistics(self, user_id):
        """load statistics if user exists"""
        with self.connection:
            stat = self.cursor.execute("SELECT user_name, games_played, games_won, games_lost, games_tied, lang FROM users WHERE user_id = %s", (user_id,)).fetchall()
            if (stat):
                stat = [{k: item[k] for k in item.keys()} for item in stat]
                return stat[0]
            return False

    def add_user(self, user_id, user_name, user_lastname):
        """register user"""
        with self.connection:
            return self.cursor.execute("INSERT INTO users (user_id, user_name, user_lastname) VALUES (%s,%s,%s)", (user_id, user_name, user_lastname,))

    def update(self, table, set, where, values):
        """update data"""
        with self.connection:
            return self.cursor.execute(f"UPDATE {table} SET {set} WHERE {where}", values)

    def close(self):
        """Close connection with DB"""
        self.connection.close()