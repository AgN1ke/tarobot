# postgresql_database.py
from .database_interface import DatabaseInterface
import psycopg2


class PostgreSQLDatabase(DatabaseInterface):
    def __init__(self, db_name='your_database', user='your_user', password='your_password', host='localhost'):
        self.conn = psycopg2.connect(dbname=db_name, user=user, password=password, host=host)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id SERIAL PRIMARY KEY,
                    first_name TEXT,
                    last_name TEXT,
                    name TEXT,
                    age TEXT,
                    gender TEXT
                )
                """)

        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS issues (
                    issue_id SERIAL PRIMARY KEY,
                    user_id INT,
                    issue TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(user_id)
                )
                """)
        self.conn.commit()

    def add_user(self, first_name, last_name, name, age, gender):
        self.cursor.execute(
            "INSERT INTO users (first_name, last_name, name, age, gender) "
            "VALUES (%s, %s, %s, %s, %s) RETURNING user_id",
            (first_name, last_name, name, age, gender))
        user_id = self.cursor.fetchone()[0]
        self.conn.commit()
        return user_id

    def user_exists(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        return self.cursor.fetchone()

    def add_issue(self, user_id, issue):
        self.cursor.execute("INSERT INTO issues (user_id, issue) VALUES (%s, %s)",
                            (user_id, issue))
        self.conn.commit()

    def close(self):
        self.conn.close()
