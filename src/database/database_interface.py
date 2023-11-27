# database_interface.py
from src.database.user import User


class DatabaseInterface:
    def create_tables(self):
        raise NotImplementedError

    def add_user(self, user: User):
        raise NotImplementedError

    def update_user(self, user: User):
        raise NotImplementedError

    def user_exists(self, user_id):
        raise NotImplementedError

    def get_user(self, user_id: int):
        raise NotImplementedError

    def add_issue(self, *args):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError
