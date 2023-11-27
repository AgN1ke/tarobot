# test_database_alchemy_pg.py
import unittest
import os
from src.database.database_factory import get_database
from src.database.user import User
from configparser import ConfigParser


class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load the configuration
        config = ConfigParser()
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            'configs', 'config.ini')
        config.read(config_path)

        # Use the 'dev' environment settings
        db_config = config['dev']

        # Construct the database URL for SQLAlchemy
        db_url = f"postgresql://{db_config.get('user')}:" \
                 f"{db_config.get('password')}@{db_config.get('host')}/{db_config.get('db_name')}"

        # Initialize the database with 'dev' configurations
        cls.db = get_database(db_type=db_config.get('db_type'), db_url=db_url)

        # Create the tables
        cls.db.create_tables()

    @classmethod
    def tearDownClass(cls):
        # Assuming that cls.db.engine is the SQLAlchemy engine instance
        cls.db.engine.dispose()

    def test_add_user(self):
        # Test adding a user
        user = User(telegram_id="12345", name="John Doe", age=30, gender="Male")
        self.db.add_user(user)

        # Verify the user was added
        retrieved_user = self.db.get_user(user.user_id)
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.name, "John Doe")

    def test_user_exists(self):
        # Test checking if a user exists
        user = User(telegram_id="54321", name="Jane Doe", age=28, gender="Female")
        self.db.add_user(user)
        self.assertTrue(self.db.user_exists(user.user_id))

    def test_update_user(self):
        # Test updating a user
        user = User(telegram_id="11111", name="Alice Smith", age=35, gender="Female")
        self.db.add_user(user)

        # Update user details
        user.name = "Alice Johnson"
        self.db.update_user(user)

        # Verify user details were updated
        updated_user = self.db.get_user(user.user_id)
        self.assertEqual(updated_user.name, "Alice Johnson")


if __name__ == '__main__':
    unittest.main()
