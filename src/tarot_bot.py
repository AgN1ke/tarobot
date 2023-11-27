# taro_bot.py
from src.database.database_interface import DatabaseInterface
from src.database.user import User
from src.gpt_assistant import GPTAssistant
from src.payment_manager import PaymentManger
from src.tarot.tarot_spread import TarotSpreadParser
from src.tarot.tarot_spread_instance import TarotSpreadInstance
from src.telegram_wrapepr import TelegramWrapper

"""
bot's workflow is:
- start command responded by greetings message
- if a user is not known to the bot ask for: name, gender, 
      birth date and adds user to the db along with telegram username is userid
- ask the user about their issue and select a most suitable spread from known spreads using gpt API
- check for account funds and start the session or inform about the fund insufficiency
- ask if the user is ok with the spread and allow them to select one manually if they don't like the selected spread
- fill the spread
- feed the spread and user data to gpt API with a request to interpret taro spread
- each card of the spread will be fed 1 by 1 and give the explanation to the user
- chat with the user regarding the spread for a limited amount of messages
- say goodbye and end the session when the limit is reached or when the user chooses to end the session
"""


class TaroBot:
    def __init__(self, telegram_id: str, chat_id: str,
                 telegram_wrapper: TelegramWrapper,
                 db_interface: DatabaseInterface,
                 gpt_assistant: GPTAssistant,
                 payment_manger: PaymentManger):
        self.telegram_id = telegram_id
        self.telegram_wrapper = telegram_wrapper
        self.chat_id = chat_id
        self.db_interface = db_interface
        self.gpt_assistant = gpt_assistant
        self.payment_manger = payment_manger

    def main_loop(self):
        self.welocome_message(self.chat_id)
        self.user_confirmation_loop(self.telegram_id)
        self.payment_loop()
        issue: str = self.ask_issue()
        spread: TarotSpreadInstance = self.spread_selection_loop(self.chat_id, issue)
        self.spread_interpretation_loop(issue, spread)
        self.chat_loop()
        self.goodbye_message(self.chat_id)

    def welocome_message(self, chat_id: str):
        self.send_telegram_message(chat_id, "Welcome to the TaroBot! Let's explore the mysteries of tarot together.")

    def user_confirmation_loop(self, telegram_id: str) -> User:
        if self.db_interface.user_exists(telegram_id):
            return self.db_interface.get_user(telegram_id)
        else:
            user = self.ask_user_info()
            self.db_interface.add_user(user)

    def ask_user_info(self) -> User:
        pass

    def payment_loop(self):
        if self.payment_manger.has_enough_funds(self.chat_id):
            self.send_telegram_message(self.chat_id, "Funds check passed. Let's continue.")
        else:
            self.send_telegram_message(self.chat_id, "Insufficient funds. Please recharge your account.")

    def ask_issue(self) -> str:
        pass

    def spread_selection_loop(self, chat_id: str, issue: str) -> TarotSpreadInstance:
        spreads = self.load_spreads()
        spread = self.select_spread_using_gpt(spreads, issue)
        if self.is_user_ok_with_spread(spread, chat_id):
            return spread
        else:
            return self.get_spread_from_user(spreads, chat_id)

    @staticmethod
    def load_spreads():
        parser = TarotSpreadParser('../../data/spreads_sample.json')
        return parser.parse_spreads()

    def select_spread_using_gpt(self, spreads, issue: str) -> TarotSpreadInstance:
        pass

    def is_user_ok_with_spread(self, spreads, chat_id: str):
        pass

    def get_spread_from_user(self, spreads, chat_id: str) -> TarotSpreadInstance:
        pass

    def spread_interpretation_loop(self, issue: str, spread: TarotSpreadInstance):
        pass

    def chat_loop(self):
        pass

    def goodbye_message(self, chat_id):
        self.send_telegram_message(chat_id, "Ok, bye.")

    def handle_user_issue(self, chat_id, issue):
        spread_suggestion = self.gpt_assistant.gpt_request(chat_id, issue, max_tokens=50)
        return spread_suggestion

    def handle_funds_check(self, chat_id):
        if self.check_user_funds(chat_id):
            self.send_telegram_message(chat_id, "Funds check passed. Let's continue.")
        else:
            self.send_telegram_message(chat_id, "Insufficient funds. Please recharge your account.")

    def select_tarot_spread(self, chat_id) -> TarotSpreadInstance | None:
        parser = TarotSpreadParser('../../data/spreads_sample.json')
        spreads = parser.parse_spreads()

        spreads_message = "Please select a tarot spread:\n"
        for idx, spread in enumerate(spreads, start=1):
            spreads_message += f"{idx}. {spread.name} - {spread.description}\n"

        self.send_telegram_message(chat_id, spreads_message)

        selected_index = self.wait_for_user_selection(chat_id)

        if 1 <= selected_index <= len(spreads):
            chosen_spread = spreads[selected_index - 1]
            spread_instance = TarotSpreadInstance(chosen_spread, '../../data/tarot_cards.json')
            return spread_instance
        else:
            self.send_telegram_message(chat_id, "Invalid selection. Please try again.")
            return None

    def wait_for_user_selection(self, chat_id) -> int:
        return 0

    def perform_tarot_reading(self, chat_id, spread):
        for card in spread:
            interpretation = self.gpt_assistant.gpt_request(chat_id, card, max_tokens=100)
            self.send_telegram_message(chat_id, interpretation)

    def interactive_chat(self, chat_id):
        pass

    def end_session(self, chat_id):
        self.send_telegram_message(chat_id, "Thank you for using TaroBot. Have a great day!")

    def send_telegram_message(self, chat_id, message):
        # Delegate message sending to TelegramWrapper
        self.telegram_wrapper.send_message(chat_id, message)

    def check_user_funds(self, chat_id):
        pass
