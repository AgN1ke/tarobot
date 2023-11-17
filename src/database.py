# database.py
import sqlite3


class DataBase:
    def __init__(self, db_name='users.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INT PRIMARY KEY,
                    first_name TEXT,
                    last_name TEXT,
                    name TEXT,
                    age TEXT,
                    gender TEXT
                )
                """)

        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS issues (
                    issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INT,
                    issue TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(user_id)
                )
                """)
        self.conn.commit()

    def add_user(self, user_id, first_name, last_name, name, age, gender):
        self.cursor.execute(
            "INSERT INTO users (user_id, first_name, last_name, name, age, gender) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, first_name, last_name, name, age, gender))
        self.conn.commit()

    def user_exists(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        return self.cursor.fetchone()

    def add_issue(self, user_id, issue):
        self.cursor.execute("INSERT INTO issues (user_id, issue) VALUES (?, ?)",
                            (user_id, issue))
        self.conn.commit()

    def close(self):
        self.conn.close()
