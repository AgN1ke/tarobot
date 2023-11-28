# test_taro_bot.py
import unittest
from unittest.mock import Mock, patch
from src.database.user import User
from src.tarot.tarot_spread_instance import TarotSpreadInstance
from src.tarot_bot import TaroBot


class TestTaroBot(unittest.TestCase):

    def setUp(self):
        # Mocking the dependencies
        self.mock_telegram_wrapper = Mock()
        self.mock_db_interface = Mock()
        self.mock_gpt_assistant = Mock()
        self.mock_payment_manager = Mock()

        # Creating a TaroBot instance with mocked dependencies
        self.bot = TaroBot(
            telegram_id="user_id",
            chat_id="chat_id",
            telegram_wrapper=self.mock_telegram_wrapper,
            db_interface=self.mock_db_interface,
            gpt_assistant=self.mock_gpt_assistant,
            payment_manager=self.mock_payment_manager
        )

    def test_welcome_message(self):
        # Test the welcome message method
        self.bot.welocome_message("chat_id")
        self.mock_telegram_wrapper.send_message.assert_called_with(
            "chat_id",
            "Welcome to the TaroBot! Let's explore the mysteries of tarot together.")

    def test_user_confirmation_loop_known_user(self):
        # Test user confirmation loop for a known user
        self.mock_db_interface.user_exists.return_value = True
        self.mock_db_interface.get_user.return_value = User()  # Assume User is a valid class

        user = self.bot.user_confirmation_loop("user_id")
        self.mock_db_interface.user_exists.assert_called_once_with("user_id")
        self.assertIsInstance(user, User)

    def test_user_confirmation_loop_new_user(self):
        # Test user confirmation loop for a new user
        self.mock_db_interface.user_exists.return_value = False
        self.bot.ask_user_info = Mock(return_value=User())  # Mock ask_user_info method

        user = self.bot.user_confirmation_loop("user_id")
        self.mock_db_interface.user_exists.assert_called_once_with("user_id")
        self.bot.ask_user_info.assert_called_once()
        self.mock_db_interface.add_user.assert_called_once()

    def test_payment_loop_sufficient_funds(self):
        # Test payment loop when there are sufficient funds
        self.mock_payment_manager.has_enough_funds.return_value = True

        self.bot.payment_loop()
        self.mock_payment_manager.has_enough_funds.assert_called_once_with("chat_id")
        self.mock_telegram_wrapper.send_message.assert_called_with("chat_id", "Funds check passed. Let's continue.")

    def test_payment_loop_insufficient_funds(self):
        # Test payment loop when there are insufficient funds
        self.mock_payment_manager.has_enough_funds.return_value = False

        self.bot.payment_loop()
        self.mock_payment_manager.has_enough_funds.assert_called_once_with("chat_id")
        self.mock_telegram_wrapper.send_message.assert_called_with("chat_id",
                                                                   "Insufficient funds. Please recharge your account.")

    def test_ask_issue(self):
        # Test the ask_issue method
        # You need to simulate a scenario where the user responds with an issue
        pass  # Replace with appropriate test logic

    def test_spread_selection_loop_user_ok_with_spread(self):
        # Test spread_selection_loop when the user is okay with the selected spread
        mock_spread = Mock(spec=TarotSpreadInstance)
        self.mock_db_interface.load_spreads.return_value = [mock_spread]
        self.mock_gpt_assistant.select_spread_using_gpt.return_value = mock_spread
        self.bot.is_user_ok_with_spread = Mock(return_value=True)

        selected_spread = self.bot.spread_selection_loop("chat_id", "issue")
        self.assertEqual(selected_spread, mock_spread)

    def test_spread_selection_loop_user_not_ok_with_spread(self):
        # Test spread_selection_loop when the user is not okay with the selected spread
        mock_spread = Mock(spec=TarotSpreadInstance)
        self.mock_db_interface.load_spreads.return_value = [mock_spread]
        self.mock_gpt_assistant.select_spread_using_gpt.return_value = mock_spread
        self.bot.is_user_ok_with_spread = Mock(return_value=False)
        self.bot.get_spread_from_user = Mock(return_value=mock_spread)

        selected_spread = self.bot.spread_selection_loop("chat_id", "issue")
        self.assertEqual(selected_spread, mock_spread)

    def test_spread_interpretation_loop(self):
        # Test the spread_interpretation_loop method
        # This would involve checking if the GPTAssistant is called for each card in the spread
        mock_spread = Mock(spec=TarotSpreadInstance)
        mock_spread.__iter__.return_value = iter(["card1", "card2"])
        self.bot.spread_interpretation_loop("issue", mock_spread)
        self.assertEqual(self.mock_gpt_assistant.gpt_request.call_count, 2)

    def test_chat_loop(self):
        # Test the chat_loop method
        # This would involve simulating a chat interaction
        pass  # Replace with appropriate test logic

    def test_goodbye_message(self):
        # Test the goodbye_message method
        self.bot.goodbye_message("chat_id")
        self.mock_telegram_wrapper.send_message.assert_called_with("chat_id",
                                                                   "Thank you for using TaroBot. Have a great day!")


if __name__ == '__main__':
    unittest.main()
