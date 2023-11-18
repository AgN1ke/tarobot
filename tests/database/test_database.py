# test_database.py
import os
import unittest
from configparser import ConfigParser
from src.database.database_factory import get_database


class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Load the configuration
        config = ConfigParser()

        config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            'configs', 'config.ini')
        config.read(config_path)

        # Use the 'dev' environment settings
        db_config = config['dev']

        # Initialize the database with 'dev' configurations
        self.db = get_database(
            db_type=db_config.get('db_type'),
            db_name=db_config.get('db_name'),
            user=db_config.get('user'),
            password=db_config.get('password'),
            host=db_config.get('host')
        )

        # Drop existing tables and recreate them
        self.db.cursor.execute("DROP TABLE IF EXISTS issues")
        self.db.cursor.execute("DROP TABLE IF EXISTS users")
        self.db.create_tables()

    def tearDown(self):
        self.db.close()

    def test_add_user(self):
        # Test adding a user
        user_id = self.db.add_user("John", "Doe", "John Doe", "30", "Male")
        self.assertIsNotNone(user_id)

    def test_user_exists(self):
        # Test checking if a user exists
        user_id = self.db.add_user("Jane", "Doe", "Jane Doe", "28", "Female")
        self.assertTrue(self.db.user_exists(user_id))

    def test_add_issue(self):
        # Test adding an issue
        user_id = self.db.add_user("Alice", "Smith", "Alice Smith", "35", "Female")
        self.db.add_issue(user_id, "Sample issue")

        # Verify the issue was added
        self.db.cursor.execute("SELECT * FROM issues WHERE user_id = %s", (user_id,))
        issue = self.db.cursor.fetchone()
        self.assertIsNotNone(issue)
        self.assertEqual(issue[1], user_id)
        self.assertEqual(issue[2], "Sample issue")


if __name__ == '__main__':
    unittest.main()
