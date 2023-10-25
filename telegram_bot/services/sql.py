# from telegram_bot.config import Config
import sqlite3


class DataBase:

    def __init__(self, db_file):
        self.connect = sqlite3.connect(db_file)
        self.cursor = self.connect.cursor()

    async def add_user(self, user_id):
        with self.connect:
            return self.cursor.execute(
                """INSERT INTO users (user_id) VALUES (?)""",
                [user_id]
            )
