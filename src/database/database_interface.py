# database_interface.py
class DatabaseInterface:
    def create_tables(self):
        raise NotImplementedError

    def add_user(self, *args):
        raise NotImplementedError

    def user_exists(self, user_id):
        raise NotImplementedError

    def add_issue(self, *args):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError
